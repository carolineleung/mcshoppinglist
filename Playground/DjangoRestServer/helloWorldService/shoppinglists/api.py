from datetime import datetime
import logging
import models
from shoppinglists.exceptions import ShoppingListError
from shoppinglists.helpers import ClassHelper, InspectHelper
from shoppinglists.models import ShoppingList, ShoppingListItem, ShoppingListDao, ShoppingListItemDao, ModelStateConstants

logger = logging.getLogger(__name__)

class ResourceNameConstants(object):
    SHOPPING_LIST_INDEX_ENTRY = 'ShoppingListIndexEntry'
    SHOPPING_LIST_INDEX = 'ShoppingListIndex'
    SHOPPING_LIST = 'ShoppingList'
    SHOPPING_LIST_ITEM = 'ShoppingListItem'

class ResourceKeys(object):
    NAME_KEY = 'name'
    ID_KEY = 'id'
    TYPE_KEY = 'type'
    STATE_KEY = 'state'
    LAST_MODIFIED_KEY = 'last_modified'
    CHECKED_KEY = 'checked'
    ITEMS_KEY = 'items'
#    LINKS_KEY = 'links'
    ENTRIES_KEY = 'entries'
    COUNT_KEY = 'count'
    LABELS_KEY = 'labels'
    ACTION_KEY = 'action'

class ActionCrudConstants(object):
    CREATE='CREATE'
    UPDATE='UPDATE'
    DELETE='DELETE'

class ShoppingListClassHelper(object):
    @staticmethod
    def check_is_shoppinglist(shopping_list_model):
        if not ClassHelper.safe_issubclass_obj(shopping_list_model, models.ShoppingList):
            raise TypeError('Expected type: ShoppingList')

class ShoppingListItemUpdateResponseFactory(object):
    def create_response_from_resource_list(self, shopping_items_list):
        return {
            'update_count': len(shopping_items_list),
            ResourceKeys.ITEMS_KEY: shopping_items_list
        }

class ShoppingListItemAdapter(object):
    def adapt_to_resource(self, shopping_item_model):
        """
        shopping_item_model: instance of class models.ShoppingListItem
        returns: resource as dict. Note that the ShoppingList FK is not included.
        """
        item_resource = {
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST_ITEM,
            ResourceKeys.ID_KEY: models.get_id_str(shopping_item_model),
        }

        if(hasattr(shopping_item_model, ResourceKeys.STATE_KEY)
            and shopping_item_model.state == ModelStateConstants.DELETED):
            # If the item was deleted, keep the resource fields sparse.
            # Include state: DELETED
            item_resource.update( {
                ResourceKeys.STATE_KEY: shopping_item_model.state
            })
        else:
            # Normal fields
            item_resource.update( {
                ResourceKeys.NAME_KEY: shopping_item_model.name,
                ResourceKeys.CHECKED_KEY: shopping_item_model.checked,
                ResourceKeys.LAST_MODIFIED_KEY: shopping_item_model.last_modified,
                ResourceKeys.LABELS_KEY: shopping_item_model.labels,
            })
        return item_resource

    def _check_resource_type(self, shopping_item_resource):
        if not InspectHelper.isdict(shopping_item_resource):
            raise ShoppingListError('Shopping item resource is invalid (Not a dict.)')

    def create_from_resource(self, shopping_item_resource, shopping_list_model):
        """
        Create a new ShoppingListItem and persist it.
        """
        self._check_resource_type(shopping_item_resource)
        ShoppingListClassHelper.check_is_shoppinglist(shopping_list_model)
        if not shopping_list_model.id:
            raise ShoppingListError('Cannot create ShoppingListItem until its '
                                    'ShoppingList is persisted. Call save() first '
                                    'on list id {0}'.format(shopping_list_model.id))
        
        item_model = ShoppingListItem()
        # foreign key link
        item_model.shopping_list = shopping_list_model
        item_model.last_modified = datetime.utcnow()
        # TODO We should sanity check values here.
        item_model.name = shopping_item_resource[ResourceKeys.NAME_KEY]
        if ResourceKeys.CHECKED_KEY in shopping_item_resource:
            item_model.checked = shopping_item_resource[ResourceKeys.CHECKED_KEY]
        else:
            item_model.checked = False
        if ResourceKeys.LABELS_KEY in shopping_item_resource:
            item_model.labels = shopping_item_resource[ResourceKeys.LABELS_KEY]
        dao = ShoppingListItemDao()
        dao.save(item_model)
        return item_model

    def update_from_resource(self, shopping_item_resource):
        """
        shopping_item_resource: ShoppingListItem as a resource dict
        """
        self._check_resource_type(shopping_item_resource)
        if not ResourceKeys.ID_KEY in shopping_item_resource:
            raise ShoppingListError('ShoppingListItem resource: missing id field.')
        item_model = None
        dao = models.ShoppingListItemDao()
        try:
            item_model = dao.get_by_id(shopping_item_resource[ResourceKeys.ID_KEY])
        except Exception:
            logger.exception('Failed to get item model by key.')
            pass
        if not item_model:
            raise ShoppingListError('Failed to find ShoppingListItem with id {0}'.format(
                shopping_item_resource[ResourceKeys.ID_KEY]))
        allowed_update_keys = [ ResourceKeys.NAME_KEY, ResourceKeys.CHECKED_KEY, ResourceKeys.LABELS_KEY ]
        should_save = False
        for resource_key in shopping_item_resource:
            if resource_key in allowed_update_keys:
                if not hasattr(item_model, resource_key):
                    raise ShoppingListError(
                        'Internal error. Model does not contain expected key: {0}'.format(resource_key))
                # Invalid values (e.g. null/None for bool) will be enforced by the DB on save
                # TODO We should sanity check values here.
                setattr(item_model, resource_key, shopping_item_resource[resource_key])
                should_save = True
        if should_save:
            item_model.last_modified = datetime.utcnow()
            # TODO Add logging
            dao.save(item_model)
        return item_model

# TODO Make all classes extend (object)
class ShoppingListAdapter(object):
    def adapt_items_list_to_resource(self, items_list):
        """
        returns: array of ShoppingListItem, i.e. [ item1, item2, itemN ], where each item is a resource (object).
        """
        adapted_items = []
        item_adapter = ShoppingListItemAdapter()
        for item in items_list:
            adapted = item_adapter.adapt_to_resource(item)
            adapted_items.append(adapted)
        return adapted_items

    def _adapt_items_to_resource(self, shopping_list_model, since_last_modified=None, include_deleted_items=False):
        dao = ShoppingListItemDao()
        items_list = dao.get_by_shopping_list_model(shopping_list_model,
            since_last_modified=since_last_modified, include_deleted_items=include_deleted_items)
        return self.adapt_items_list_to_resource(items_list)

    # TODO Introduce parameter object for: since_last_modified=None, include_deleted_items=False
    def adapt_to_resource(self, shopping_list_model, include_items=True,
                          since_last_modified=None, include_deleted_items=False):
        """
        shopping_list_model: instance of class models.ShoppingList
        """
        ShoppingListClassHelper.check_is_shoppinglist(shopping_list_model)

        # Return a "sparse" ShoppingList if last_modified <= since_last_modified
        # Currently, we only have "name" that can be updated by users,
        # so that's the only field that's taken out if not updated.
        resource = {
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST,
            ResourceKeys.ID_KEY: models.get_id_str(shopping_list_model),
            ResourceKeys.LAST_MODIFIED_KEY: shopping_list_model.last_modified,
        }
        if not since_last_modified or shopping_list_model.last_modified > since_last_modified:
            resource[ResourceKeys.NAME_KEY] = shopping_list_model.name

        # Get the items in the shopping list
        if include_items:
            adapted_items = self._adapt_items_to_resource(shopping_list_model,
                since_last_modified, include_deleted_items)
            resource[ResourceKeys.ITEMS_KEY] = adapted_items

        return resource

    def _check_resource_type(self, shopping_list_resource):
        if not InspectHelper.isdict(shopping_list_resource):
            raise ShoppingListError('Shopping list resource is invalid (Not a dict.)')

    def _update_shopping_list_model(self, shopping_list_resource, list_model, include_items=True):
        """
        Update fields and persist (ShoppingListModel) list_model. Create new items.
        """
        if ResourceKeys.NAME_KEY in shopping_list_resource:
            list_model.name = shopping_list_resource[ResourceKeys.NAME_KEY]
        list_model.last_modified = datetime.utcnow()
        dao = models.ShoppingListDao()
        dao.save(list_model)

        if include_items:
            if ResourceKeys.ITEMS_KEY in shopping_list_resource:
                items = shopping_list_resource[ResourceKeys.ITEMS_KEY]
                if InspectHelper.isiterable(items):
                    item_adapter = ShoppingListItemAdapter()
                    for item_resource in items:
                        item_adapter.create_from_resource(item_resource, list_model)

        # Refresh the model (e.g. if there were triggers or a sproc that changed something other than the above)
        refreshed_list_model = None
        try:
            dao = ShoppingListDao()
            refreshed_list_model = dao.get_by_id(list_model.id)
        except Exception:
            # TODO log
            raise
        if not refreshed_list_model:
            raise ShoppingListError('Failed to refresh ShoppingList after '
                                    'update, id: {0}'.format(list_model.id))
        return refreshed_list_model

    def create_from_resource(self, shopping_list_resource):
        """
        Create a new ShoppingList, its items, and persist it.
        
        shopping_list_resource: dict of a shopping_list_model, per adapt_to_resource.
        """
        self._check_resource_type(shopping_list_resource)
        list_model = ShoppingList()
        list_model = self._update_shopping_list_model(shopping_list_resource, list_model)
        return list_model

    def update_from_resource(self, expected_list_id, shopping_list_resource, include_items=True):
        """
        Perform a full update (replacement) of the ShoppingList. All old items are deleted.
        
        shopping_list_resource: dict of a shopping_list_model, per adapt_to_resource.
        """
        self._check_resource_type(shopping_list_resource)
        if not ResourceKeys.ID_KEY in shopping_list_resource:
            raise ShoppingListError('Invalid shopping list resource. '
                + 'Failed to find shopping list key: {0}'.format(ResourceKeys.ID_KEY))
        shopping_list_id = shopping_list_resource[ResourceKeys.ID_KEY]
        if unicode(expected_list_id) != unicode(shopping_list_id):
            raise ShoppingListError('Invalid shopping list resource. '
                + 'The resource shopping list id: {0} does not '
                + 'match the requested URI id: {1}'.format(expected_list_id, shopping_list_id))
        try:
            dao = ShoppingListDao()
            list_model = dao.get_by_id(shopping_list_id)
        except Exception:
            # TODO log
            pass
        if not list_model:
            raise ShoppingListError('Failed to find shopping list with id: {0}'.format(shopping_list_id))
        if include_items:
            # Delete all ShoppingListItem for the list.
            dao = ShoppingListItemDao()
            dao.mark_items_deleted(list_model)
        # Update fields on the ShoppingList, and create new items
        list_model = self._update_shopping_list_model(shopping_list_resource, list_model, include_items=include_items)
        return list_model



class ShoppingListIndexEntryAdapter(object):
    """
    shopping_list_model: instance of class models.ShoppingList
    """
    def adapt_to_resource(self, shopping_list_model):
#        links = [ LinkFactory.create_shopping_list_link(shopping_list_model.id) ]
        return {
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST_INDEX_ENTRY,
            ResourceKeys.ID_KEY: models.get_id_str(shopping_list_model),
            #ResourceKeys.LINKS_KEY: links
        }

class ShoppingListIndexAdapter(object):
    def adapt_to_resource(self):
        entry_adapter = ShoppingListIndexEntryAdapter()
        entries = []
        # TODO Add limit / pagination?
        dao = ShoppingListDao()
        for shopping_list_model in dao.get_all():
            adapted = entry_adapter.adapt_to_resource(shopping_list_model)
            entries.append(adapted)
        return {
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST_INDEX,
            ResourceKeys.COUNT_KEY: len(entries),
            ResourceKeys.ENTRIES_KEY: entries
        }





## Force JSON to avoid adding ?format=json https://github.com/toastdriven/django-tastypie/issues/issue/40
## in Meta: serializer = create_json_serializer()
#def create_json_serializer():
#    return Serializer(formats=['json', 'jsonp'],
#        content_types = {'json': 'application/json', 'jsonp': 'text/javascript'}
#    )


#class MyQuerySet:
#    def __init__(self, obj_list):
#        self.obj_list = obj_list
#    def count(self):
#        return len(self.obj_list)
#    def __iter__(self):
#        return self
#    def __getitem__(self, item):
#        return self.obj_list[item]
#    def next(self):
#        for obj in self.obj_list:
#            yield obj

#class MySerializable:
#    def __init__(self, id = 0):
#        self.id = id

#class ShoppingListResource(MySerializable):
#    """
#    items: list of ShoppingListItemResource
#    """
#    def __init__(self, id = 0, name = '', items = [], last_modified = None, changelist=0):
#        MySerializable.__init__(self, id)
#        self.name = name
#        self.items = items
#        self.last_modified = last_modified
#        self.changelist = changelist
#        self.debug_null_ref = None
#        self.type = 'ShoppingList'
#
#class ShoppingListItemResource(MySerializable):
#    def __init__(self, name = '', id = 0, checked = False, last_modified = None, changelist=0):
#        MySerializable.__init__(self, id)
#        self.name = name
#        self.checked = checked
#        self.last_modified = last_modified
#        self.changelist = changelist
#        self.type = 'ShoppingListItem'

#class LinkResource:
#    def __init__(self, rel = '', uri = ''):
#        self.rel = rel
#        self.uri = uri
#        self.type = 'Link'

#class ShoppingListIndexEntryResource:
#    def __init__(self, id = 0, links = []):
#        """
#        links: list of LinkResource
#        """
#        self.id = id
#        self.links = links
#        self.type = 'ShoppingListIndexEntry'
#
#class ShoppingListIndexResource:
#    def __init__(self, count = 0, entries = []):
#        self.count = count
#        self.entries = entries
#        self.type = 'ShoppingListIndex'

