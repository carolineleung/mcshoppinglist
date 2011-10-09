from mcshoppinglist.api.views.diffview import ShoppingListDiffView
from mcshoppinglist.api.views.indexview import ShoppingListIndexView
from mcshoppinglist.api.views.itemview import ShoppingListItemView
from mcshoppinglist.api.views.listview import ShoppingListView
from mcshoppinglist.shared.handlerwrapper import RequestHandlerWrapper

# TODO In all responses, tweak response headers, mime type etc.: http://blog.nullobject.ca/2010/02/08/django-json-woes/
# TODO Add Location headers where appropriate for new resources. (Updated too? Check http spec.)
# TODO Idempotent DELETE, particularly of entire shopping lists!   The DELETE method is idempotent. This implies that the server must return response code 200 (OK) even if the server deleted the resource in a previous request. But in practice, implementing DELETE as an idempotent operation requires the server to keep track of all deleted resources. Otherwise, it can return a 404 (Not Found).


def shopping_list_index(request):
    view = ShoppingListIndexView()
    return RequestHandlerWrapper.handle(view.shopping_list_index_handler, request)

def shopping_list_detail(request):
    view = ShoppingListView()
    return RequestHandlerWrapper.handle(view.shopping_list_detail_handler, request)

def shopping_list_meta(request):
    view = ShoppingListView()
    return RequestHandlerWrapper.handle(view.shopping_list_meta_handler, request)

def shopping_list_items(request):
    view = ShoppingListItemView()
    return RequestHandlerWrapper.handle(view.shopping_list_items_handler, request)

def shopping_list_diff(request):
    view = ShoppingListDiffView()
    return RequestHandlerWrapper.handle(view.shopping_list_diff_handler, request)

