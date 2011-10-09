from mcshoppinglist.shared.requestdata import RequestSingleton
from mcshoppinglist.shoppinglists.dao import ShoppingListDao

#def shopping_list_editor(request):
#    dao = ShoppingListDao()
#    all_shopping_lists = dao.get_all()
##    return render_to_response('shoppinglisteditor/shopping_list_static_editor.html',
##                              {
##                                  'STATIC_DOC_ROOT': settings.STATIC_DOC_ROOT,
##                                  'all_shopping_lists': all_shopping_lists,
##                              })
#    raise Exception('Not impl')

def shopping_list_editor_legacy(request):
    RequestSingleton(request)
    dao = ShoppingListDao()
    all_shopping_lists = dao.get_all()
#    return render_to_response('shoppinglisteditor/shopping_list_entry_editor.html',
#                              {
#                                  'STATIC_DOC_ROOT': settings.STATIC_DOC_ROOT,
#                                  'all_shopping_lists': all_shopping_lists,
#                              })
    return {
        'static_content_path': '/static', # TODO Push this out to settings/config file.
        'all_shopping_lists': all_shopping_lists
    }
