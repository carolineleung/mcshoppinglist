# http://docs.python.org/library/datetime.html#strftime-strptime-behavior
# datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
from datetime import datetime
from mcshoppinglist.api.constants import ResourceKeys, ResourceNameConstants
from mcshoppinglist.shoppinglists.dao import ShoppingListDao, ShoppingListItemDao
from mcshoppinglist.shoppinglists.models import ShoppingList, ShoppingListItem

SHARED_DATETIME = datetime(2011, 02, 15, 21, 15, 38)


class ShoppingListTestDataOneItem:
    def __init__(self):
        # A short test shopping list
        self.newList1 = ShoppingList()
        self.newList1.name = 'Test List Name 1'
        self.newList1.last_modified = SHARED_DATETIME
        dao = ShoppingListDao()
        dao.save(self.newList1)

        self.newItem1 = self.create_and_save_new_item(self.newList1, 'item1 in list: ' + self.newList1.name)

        # A shopping list as resource
        self.shopping_list_resource2 = {
            ResourceKeys.NAME_KEY: 'Test List Name 2 (From Resource)',
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST,
            ResourceKeys.ITEMS_KEY: [
                self.create_item_resource('item1 bok choi'),
                self.create_item_resource('item2 gai lan', True),
                self.create_item_resource('item3 bananas'),
            ]
        }

    def create_item_resource(self, name, checked=False):
        return {
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST_ITEM,
            ResourceKeys.NAME_KEY: name,
            ResourceKeys.CHECKED_KEY: checked,
        }

    def create_and_save_new_item(self, shopping_list, item_name):
        newItem1 = ShoppingListItem()
        newItem1.shopping_list = shopping_list
        newItem1.name = '' + item_name
        newItem1.checked = False
        newItem1.last_modified = SHARED_DATETIME
        dao = ShoppingListItemDao()
        dao.save(newItem1)
        return newItem1