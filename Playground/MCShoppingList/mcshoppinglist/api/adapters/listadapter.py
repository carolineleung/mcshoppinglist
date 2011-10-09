from datetime import datetime
from mcshoppinglist.api.adapters.itemadapter import ShoppingListItemAdapter
from mcshoppinglist.api.helpers import ShoppingListClassHelper
from mcshoppinglist.shared.exceptions import  ShoppingListError
from mcshoppinglist.shared.helpers import InspectHelper
from mcshoppinglist.shared.logfactory import LogFactory
from mcshoppinglist.shared.models.helpers import get_id_str
from mcshoppinglist.api.constants import ResourceKeys, ResourceNameConstants
from mcshoppinglist.shoppinglists.dao import ShoppingListItemDao, ShoppingListDao
from mcshoppinglist.shoppinglists.models import ShoppingList

logger = LogFactory.get_logger(__name__)

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
            ResourceKeys.ID_KEY: get_id_str(shopping_list_model),
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
        dao = ShoppingListDao()
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
