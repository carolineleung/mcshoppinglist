# NOTE: If you see this error:
#   ConfigurationExecutionError: <type 'exceptions.TypeError'>: object of type 'NoneType' has no len()
#   in:  ('....mcshoppinglist\\routes.py', 28, 'add_url_dispatch_routes'
# It means that one of your (pyramid) view callables has MORE required parameters than just the webob request.
# Check your view callable method declaration.
from pyramid.exceptions import Forbidden
from mcshoppinglist.auth.authentication import AuthenticationManager


def add_api_routes(config):
    from mcshoppinglist.api.viewentrypoints import shopping_list_detail, shopping_list_index, shopping_list_meta, shopping_list_items, shopping_list_diff
    prefix_no_trailing_slash = '/api/v1/shoppinglists'
    prefix = prefix_no_trailing_slash + '/'

    # We want optional trailing slashes r'/?' on our resource URLs.
    # TODO Is there a better optional trailing slashes than this unused param: {unused:/?}. We could set up redirects per the Pyramid docs, but why make the extra request?
    # TODO Do these route strings need to be regex escaped? e.g. r'^(?P<list_id>\d+)/item/(?P<item_id>)/?$'

    # /
    # GET: index of ShoppingList
    # POST: create a new ShoppingList
    config.add_route('api_shopping_list_index', prefix_no_trailing_slash + '{unused:/?}',
                     view=shopping_list_index)

    # GET: the ShoppingList and its ShoppingListItem list
    # PUT: update and overwrite all ShoppingList details (deletes all old items).
    # DELETE: delete the ShoppingList and all its items.
    #(r'^(?P<list_id>[a-zA-Z0-9]+)/?$', 'shopping_list_detail'),
    config.add_route('api_shopping_list_detail', prefix + '{list_id:[a-zA-Z0-9]+}{unused:/?}',
                     view=shopping_list_detail)

    # GET: the ShoppingList metadata but not its items.
    # PUT: update and overwrite all ShoppingList metadata. The items are unchanged.
    config.add_route('api_shopping_list_meta', prefix + '{list_id:[a-zA-Z0-9]+}/meta{unused:/?}',
                     view=shopping_list_meta)

    # POST: Message body: { action: "act", items: [ {item1}, {item2}...] }
    # Where action is one of: CREATE, UPDATE, DELETE.
    #
    # CREATE: create new ShoppingListItem(s) from the supplied items list, ShoppingListItem.id is ignored.
    # UPDATE: update only the supplied ShoppingListItem list items. Items can be sparse (missing fields), e.g. only provide checked state.
    # DELETE: Delete the specified items, each item only requires the ShoppingListItem.id.
    config.add_route('api_shopping_list_items', prefix + '{list_id:[a-zA-Z0-9]+}/items{unused:/?}',
                     view=shopping_list_items)

    # GET:
    #  With If-Modified-Since/If-None-Match:
    #  Only items changed since the ShoppingList and its ShoppingListItem list
    #  Without conditional: All items in the list.
    #  Message body is the same as /<list_id>/ i.e. ShoppingList with a list of ShoppingListItems,
    #  but only data changed since If-Modified-Since/If-None-Match are included.
    config.add_route('api_shopping_list_diff', prefix + '{list_id:[a-zA-Z0-9]+}/diff{unused:/?}',
                     view=shopping_list_diff)

    # TODO Act on a single item. GET, POST, DELETE
    #(r'^(?P<list_id>\d+)/item/(?P<item_id>)/?$', 'shopping_items_delete_single'),


def add_editor_routes(config):
    from mcshoppinglist.shoppinglisteditor.views import shopping_list_editor_legacy
    prefix = '/editor/'

    config.add_route('editor_legacy1', pattern=prefix + 'legacy1{unused:/?}',
                     view=shopping_list_editor_legacy, renderer='shoppinglisteditor/editor_legacy1.mako',
                     permission=AuthenticationManager.PERMISSION_ACCESS)
    config.add_route('editor_legacy2', pattern=prefix + 'legacy2{unused:/?}',
                     view=shopping_list_editor_legacy, renderer='shoppinglisteditor/editor_legacy2.mako',
                     permission=AuthenticationManager.PERMISSION_ACCESS)
    config.add_static_view(name='static', path='mcshoppinglist:static/')

    # TODO static url for /

def add_login_routes(config):
    from mcshoppinglist.login.viewentrypoints import login_empty_interstitial1, login_api_login, login_interstitial1, login_redirect
    config.add_route('login_interstitial1', pattern='/login{unused:/?}',
                     view=login_interstitial1, renderer='login/login_interstitial1.mako')
    config.add_route('login_signup_interstitial1', pattern='/login/signup{unused:/?}',
                     view=login_empty_interstitial1, renderer='login/signup_interstitial1.mako')
    config.add_route('login_api_login', pattern='/login/api/login{unused:/?}',
                     view=login_api_login)

    config.add_view(view=login_redirect, context=Forbidden, renderer='login/login_interstitial1.mako')

def add_url_dispatch_routes(config):
    add_api_routes(config)
    add_editor_routes(config)
    add_login_routes(config)




