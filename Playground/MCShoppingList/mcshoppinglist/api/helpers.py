from mcshoppinglist.api.constants import ResourceKeys
from mcshoppinglist.shared.helpers import ClassHelper
from mcshoppinglist.shoppinglists.models import ShoppingList

class ShoppingListClassHelper(object):
    @staticmethod
    def check_is_shoppinglist(shopping_list_model):
        if not ClassHelper.safe_issubclass_obj(shopping_list_model, ShoppingList):
            raise TypeError('Expected type: ShoppingList')

class ShoppingListItemUpdateResponseFactory(object):
    def create_response_from_resource_list(self, shopping_items_list):
        return {
            'update_count': len(shopping_items_list),
            ResourceKeys.ITEMS_KEY: shopping_items_list
        }
