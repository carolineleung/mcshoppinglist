# Note that the below import sets handler404: http://docs.djangoproject.com/en/dev/intro/tutorial03/
from django.conf.urls.defaults import patterns

# TODO Ensure this /items/ URI stays in sync between urls.py and api.py.
# TODO Is there any way to DRY this /items/ path with urls.py and api.py?

urlpatterns = patterns('shoppinglists.views',
    # /
    # GET: index of ShoppingList
    # POST: create a new ShoppingList
    (r'^$', 'shopping_list_index'),

    # GET: the ShoppingList and its ShoppingListItem list
    # PUT: update and overwrite all ShoppingList details (deletes all old items).
    # DELETE: delete the ShoppingList and all its items.
    (r'^(?P<list_id>[a-zA-Z0-9]+)/?$', 'shopping_list_detail'),

    # GET: the ShoppingList metadata but not its items.
    # PUT: update and overwrite all ShoppingList metadata. The items are unchanged.
    (r'^(?P<list_id>[a-zA-Z0-9]+)/meta/?$', 'shopping_list_meta'),

    # POST: Message body: { action: "act", items: [ {item1}, {item2}...] }
    # Where action is one of: CREATE, UPDATE, DELETE.
    #
    # CREATE: create new ShoppingListItem(s) from the supplied items list, ShoppingListItem.id is ignored.
    # UPDATE: update only the supplied ShoppingListItem list items. Items can be sparse (missing fields), e.g. only provide checked state.
    # DELETE: Delete the specified items, each item only requires the ShoppingListItem.id.
    (r'^(?P<list_id>[a-zA-Z0-9]+)/items/?$', 'shopping_list_items'),

    # GET:
    #  With If-Modified-Since/If-None-Match:
    #  Only items changed since the ShoppingList and its ShoppingListItem list
    #  Without conditional: All items in the list.
    #  Message body is the same as /<list_id>/ i.e. ShoppingList with a list of ShoppingListItems,
    #  but only data changed since If-Modified-Since/If-None-Match are included.
    (r'^(?P<list_id>[a-zA-Z0-9]+)/diff/?$', 'shopping_list_diff'),

    # TODO Act on a single item. GET, POST, DELETE
    #(r'^(?P<list_id>\d+)/item/(?P<item_id>)/?$', 'shopping_items_delete_single'),
)

#
# TODO Remove this. It was originally for linkrels REST method discovery, but we're removing these for simplicity.
#
## Ensure these /items/ URIs stay in sync between this and urlpatterns
## TODO Is there any way to DRY this /items/ path with urls.py and api.py?
#class LinkFactory(object):
#    LINK_RELS = '/linkrels'
#    SHOPPING_LIST_LINK_REL = LINK_RELS + '/shopping_list'
#    SHOPPING_ITEMS_PARTIAL_UPDATE_LINK_REL = LINK_RELS + '/shopping_list/items/partial_update'
#    SELF_REL = 'self'
#
#    @staticmethod
#    def create_shopping_list_self_link(shopping_list_id):
#        return {
#            'rel': LinkFactory.SELF_REL,
#            'uri': '/%s/' % shopping_list_id
#        }
#
#    @staticmethod
#    def create_shopping_item_self_link(shopping_list_id, shopping_item_id):
#        return {
#            'rel': LinkFactory.SELF_REL,
#            'uri': '/%s/items/%s/' % (shopping_list_id, shopping_item_id)
#        }
#
#    @staticmethod
#    def create_shopping_list_link(shopping_list_id):
#        return {
#            'rel': LinkFactory.SHOPPING_LIST_LINK_REL,
#            'uri': '/%s/' % shopping_list_id
#        }
#
#    @staticmethod
#    def create_shopping_item_update_link(shopping_list_id):
#        return {
#            'rel': LinkFactory.SHOPPING_ITEMS_PARTIAL_UPDATE_LINK_REL,
#            'uri': '/%s/items/diff/' % shopping_list_id
#        }
