from datetime import datetime

# This date will be overridden in api.
from bson.objectid import ObjectId
from mongoengine.document import Document
from mongoengine.fields import StringField, StringField, DateTimeField, IntField, ReferenceField, BooleanField
import dependencyresolver
from shoppinglists.exceptions import ShoppingListError

DEFAULT_DATE=datetime(2011, 01, 01)
INVALID_ID = -1

class ModelStateConstants(object):
    LIVE = 'LIVE'
    DELETED = 'DELETED'
    ALL_STATES = { LIVE, DELETED }

DEFAULT_STATE = ModelStateConstants.LIVE

def _fix_state(model):
    if not hasattr(model, 'state') or not model.state in ModelStateConstants.ALL_STATES:
        model.state = DEFAULT_STATE

def get_id_str(doc):
    """
    Avoid using MongoEngine Document self.id which returns an instance of ObjectId
    and if converted to a str uses repr: ObjectId('4d7d0785cf66075114000002')
    Instead, this returns the hash string '4d7d0785cf66075114000002' via str().
    """
    if not hasattr(doc, 'id'):
        raise ShoppingListError('No id property found for doc: {0}'.format(doc))
    id = str(doc.id)
    if not id:
        raise ShoppingListError('Missing id for doc: {0}'.format(doc))
    return id

class ShoppingList(Document):
    name = StringField(max_length=200)
    last_modified = DateTimeField(default=DEFAULT_DATE)
    state = StringField(max_length=10, min_length=1, default=ModelStateConstants.LIVE)

    #def save(self, force_insert=False, force_update=False, using=None):
    def save(self, *args, **kwargs):
        self.last_modified = datetime.utcnow()
        _fix_state(self) # TODO Revisit this ugly way of guaranteeing state
        # super.save() first to ensure an id is assigned
        super(ShoppingList, self).save(*args, **kwargs)
        try:
            etag_manager = dependencyresolver.DependencyResolver.get_etag_manager()
            etag_manager.save_etag(self)
        except Exception as ex:
            raise ShoppingListError('Failed to save etag. ShoppingList id: {0}'.format(self.id), ex)

class ShoppingListItem(Document):
    # TODO Revise to use id instead?
    shopping_list = ReferenceField(ShoppingList)
    name = StringField(max_length=200, default='')
    checked = BooleanField(default=False)
    last_modified = DateTimeField(default=DEFAULT_DATE)
    labels = StringField(max_length=300, default='')
    state = StringField(max_length=10, min_length=1, default=ModelStateConstants.LIVE)

    #def save(self, force_insert=False, force_update=False, using=None):
    def save(self, *args, **kwargs):
        self.last_modified = datetime.utcnow()
        _fix_state(self) # TODO Revisit this ugly way of guaranteeing state
        super(ShoppingListItem, self).save(*args, **kwargs)
        try:
            etag_manager = dependencyresolver.DependencyResolver.get_etag_manager()
            # Use the ShoppingList for ETag id, but our ShoppingListItem last_modified.
            # This routes both ShoppingList and ShoppingListItem to the same ETag.
            etag_manager.save_etag(self.shopping_list, self.last_modified)
        except Exception as ex:
            raise ShoppingListError('Failed to save etag. ShoppingListItem id: {0}'.format(self.id), ex)

    def __unicode__(self):
        return 'name: {0}, id: {1}'.format(self.name, self.id)


# TODO Move this over to etags package
class EtagCacheEntry(Document):
    #  str(bson.ObjectId) i.e. the string hex value of the model's mongoengine/mongodb ObjectId. Note that mongoengine Document.id is a bson.ObjectId instance; call str on it.
    target_model_id = StringField(min_length=1)
    target_category = StringField(max_length=200)
    # TODO Add an index on etag
    etag = StringField(max_length=200)
    last_modified = DateTimeField(default=DEFAULT_DATE)

    def save(self, *args, **kwargs):
        self.last_modified = datetime.utcnow()
        super(EtagCacheEntry, self).save(*args, **kwargs)
    

class DaoBase(object):
    def delete(self, model):
        model.state = ModelStateConstants.DELETED
        model.save()

    def save(self, model):
        model.save()

    def get_by_id_from_objects(self, id, model_objects):
        """
        model_objects: ShoppingListItem.objects
        """
        model = None
        try:
            # TODO can we use Document.objects(id=objid) to avoid the exception handling? get() raises DoesNotExist.
            # Auto wrapped if id is already an ObjectId. Auto converted to ObjectId if id is hex string.
            model = model_objects.get(id=id)
        except Exception:
            # ignore
            pass
        return model

class ShoppingListDao(DaoBase):
    def get_count(self):
        # TODO Does this RETRIEVE all documents??? More efficient way to get a count?
        return self.get_all().count()
    
    def get_all(self):
        return ShoppingList.objects.filter(state__ne=ModelStateConstants.DELETED)

    def get_by_id(self, id):
        return self.get_by_id_from_objects(id, ShoppingList.objects)

class ShoppingListItemDao(DaoBase):
    def get_by_id(self, id, shopping_list_model=None):
        """
        shopping_list_model: when not None, restrict the get to only
        """
        if shopping_list_model:
            qs = ShoppingListItem.objects.filter(id=id, shopping_list=shopping_list_model)
            # TODO Assert? Should never be more than one matching exact id!
            if qs and qs.count() > 0 and qs[0]:
                return qs[0]
            return None
        else:
            return self.get_by_id_from_objects(id, ShoppingListItem.objects)

    def get_by_shopping_list_model(self, shopping_list_model, since_last_modified=None, include_deleted_items=False):
        filter_kwargs = { 'shopping_list': shopping_list_model }

        if since_last_modified:
            filter_kwargs['last_modified__gt'] = since_last_modified
        if not include_deleted_items:
            filter_kwargs['state__ne'] = ModelStateConstants.DELETED

        return ShoppingListItem.objects.filter(**filter_kwargs)

    def mark_item_deleted(self, item_model):
        item_model.state = ModelStateConstants.DELETED
        item_model.save()

    def mark_items_deleted(self, shopping_list_model):
        """
        shopping_list_model: a ShoppingList model
        """
        delete_items_queryset = ShoppingListItem.objects.filter(shopping_list=shopping_list_model)
        if delete_items_queryset and delete_items_queryset.count() > 0:
            # delete_items_queryset.delete()
            for item_to_delete in delete_items_queryset:
                self.mark_item_deleted(item_to_delete)

class EtagCacheEntryDao(DaoBase):
    def get_by_id(self, id):
        return self.get_by_id_from_objects(id, EtagCacheEntry.objects)

    def get_by_target(self, target_model_id, target_category):
        id = str(target_model_id)
        return EtagCacheEntry.objects.filter(target_model_id=id, target_category=target_category)