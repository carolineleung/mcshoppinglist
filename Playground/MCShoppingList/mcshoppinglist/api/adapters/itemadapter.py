from datetime import datetime
from mcshoppinglist.api.helpers import ShoppingListClassHelper
from mcshoppinglist.shared.exceptions import ShoppingListError
from mcshoppinglist.shared.helpers import InspectHelper
from mcshoppinglist.shared.logfactory import LogFactory
from mcshoppinglist.shared.models.constants import ModelStateConstants
from mcshoppinglist.shared.models.helpers import get_id_str
from mcshoppinglist.api.constants import ResourceKeys, ResourceNameConstants
from mcshoppinglist.shoppinglists.dao import ShoppingListItemDao
from mcshoppinglist.shoppinglists.models import ShoppingListItem

logger = LogFactory.get_logger(__name__)

class ShoppingListItemAdapter(object):
    def adapt_to_resource(self, shopping_item_model):
        """
        shopping_item_model: instance of class models.ShoppingListItem
        returns: resource as dict. Note that the ShoppingList FK is not included.
        """
        item_resource = {
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST_ITEM,
            ResourceKeys.ID_KEY: get_id_str(shopping_item_model),
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
        dao = ShoppingListItemDao()
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