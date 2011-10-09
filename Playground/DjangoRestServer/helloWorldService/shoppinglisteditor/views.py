from django.shortcuts import render_to_response
import settings
from shoppinglists.models import ShoppingList, ShoppingListDao

def shopping_list_editor(request):
    dao = ShoppingListDao()
    all_shopping_lists = dao.get_all()
    return render_to_response('shoppinglisteditor/shopping_list_static_editor.html',
                              {
                                  'STATIC_DOC_ROOT': settings.STATIC_DOC_ROOT,
                                  'all_shopping_lists': all_shopping_lists,
                              })

def shopping_list_editor2(request):
    dao = ShoppingListDao()
    all_shopping_lists = dao.get_all()
    return render_to_response('shoppinglisteditor/shopping_list_entry_editor.html',
                              {
                                  'STATIC_DOC_ROOT': settings.STATIC_DOC_ROOT,
                                  'all_shopping_lists': all_shopping_lists,
                              })
