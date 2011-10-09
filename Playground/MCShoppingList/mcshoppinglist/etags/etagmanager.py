import base64
from datetime import datetime
from mcshoppinglist.etags.dao import EtagCacheEntryDao
from mcshoppinglist.shared.exceptions import ShoppingListError
from mcshoppinglist.shoppinglists.models import ShoppingList, ShoppingListItem

# TODO Rename to something else..?
class EtagManager(object):
    # http://docs.python.org/library/datetime.html#strftime-strptime-behavior
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S:%f'
    SHOPPING_LIST_TAG = 'ShoppingList'

    def _get_category(self, obj):
        # TODO This won't work with duck typing
        obj_class = None
        if obj:
            obj_class = obj.__class__
        # TODO Rather than type checking here, can we use duck typing / hasattr to do this in a better way that decouples this from the ShoppingList class?
        if issubclass(obj_class, ShoppingList) or issubclass(obj_class, ShoppingListItem):
            return EtagManager.SHOPPING_LIST_TAG
        raise ShoppingListError('Failed to map type to tag for object: {0}'.format(obj))

    def generate_etag(self, model_for_etag, last_modified_for_etag):
        if not model_for_etag:
            raise ShoppingListError('Either a list or item parameter must be specified.')

        target_tag = self._get_category(model_for_etag)
        # last_modified = model_for_etag.last_modified
        last_modified = last_modified_for_etag.strftime(EtagManager.DATETIME_FORMAT)
        model_id = model_for_etag.id

        # Updating this format requires that you also update get_changelist_from_etag()
        etag_u = unicode('{0}|{1}|{2}'.format(target_tag, model_id, last_modified))
        return base64.b64encode(etag_u)

    def _decode_etag(self, etag_b64):
        """
        etag_b64: base64 encoded etag.
        returns: base64 decoded etag.
        """
        if not etag_b64:
            raise ShoppingListError('Invalid (empty) etag parameter.')
        try:
            return base64.b64decode(etag_b64)
        except Exception as ex:
            raise ShoppingListError('Failed to decode etag. Cause: {0}  Etag: {1}'.format(ex.message, etag_b64), ex)

    def get_last_modified_from_etag(self, etag_b64):
        from datetime import datetime
        etag = self._decode_etag(etag_b64)
        if not etag:
            raise ShoppingListError('Invalid (empty) etag parameter.')
        parts = etag.split('|')
        if not parts or len(parts) < 3:
            raise ShoppingListError('Failed to parse last_modified in etag parameter.')
        last_modified = None
        try:
            last_modified = parts[2]
            last_modified = datetime.strptime(last_modified, EtagManager.DATETIME_FORMAT)
        except Exception as ex:
            raise ShoppingListError('Failed to parse last_modified: {0}    in etag: {1}'.format(last_modified, etag), ex)
        return last_modified

    def save_etag(self, model_for_etag, last_modified_for_etag=None):
        if not last_modified_for_etag:
            last_modified_for_etag = model_for_etag.last_modified
        etag = self.generate_etag(model_for_etag, last_modified_for_etag)
        # django error on save: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings (like text_factory = str). It is highly recommended that you instead just switch your application to Unicode strings.
        #etag = unicode(etag)

        etag_model = self.get_etag_model(model_for_etag)

        dao = EtagCacheEntryDao()
        if not etag_model:
            etag_model = dao.create_etag_cache_entry()

        etag_model.target_model_id = str(model_for_etag.id)
        etag_model.target_category = self._get_category(model_for_etag)
        etag_model.etag = etag
        etag_model.last_modified = datetime.utcnow()
        dao.save(etag_model)
        return etag_model

    def get_etag_model(self, model_for_etag):
        target_category = self._get_category(model_for_etag)
        dao = EtagCacheEntryDao()
        etag_queryset = dao.get_by_target(model_for_etag.id, target_category)
        if etag_queryset.count() <= 0 or not etag_queryset[0]:
            return None
        # TODO If there's more than one, that's an error we should clean up
        if etag_queryset.count() > 1:
            raise ShoppingListError('Multiple etags found for model with id: '
                                    '{0}  category: {1}'.format(model_for_etag.id, target_category))
        return etag_queryset[0]

#    def get_etag(self, model_for_etag):
#        return self.get_etag_model(model_for_etag).etag;

    def delete_etag(self, model_for_etag=None):
        raise ShoppingListError('Not implemented ' + model_for_etag)


