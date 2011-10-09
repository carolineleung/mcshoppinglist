from mcshoppinglist.api.constants import ResourceKeys, ResourceNameConstants
from mcshoppinglist.shared.logfactory import LogFactory
from mcshoppinglist.shared.models.helpers import get_id_str
from mcshoppinglist.shoppinglists.dao import  ShoppingListDao

logger = LogFactory.get_logger(__name__)

class ShoppingListIndexEntryAdapter(object):
    """
    shopping_list_model: instance of class models.ShoppingList
    """
    def adapt_to_resource(self, shopping_list_model):
#        links = [ LinkFactory.create_shopping_list_link(shopping_list_model.id) ]
        return {
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST_INDEX_ENTRY,
            ResourceKeys.ID_KEY: get_id_str(shopping_list_model),
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

