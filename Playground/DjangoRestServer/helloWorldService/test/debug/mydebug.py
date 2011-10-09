#from datetime import datetime
#import os
#import sys
#
## TODO Use path relative to... what?
#sys.path.append('M:/src/_personal/pywebplayground/Playground/helloWorldService')
#sys.path.append('C:/mel/hg-repo/pywebplayground/Playground/helloWorldService')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from shoppinglists.models import ShoppingList, ShoppingListItem
#
#print('Python %s on %s' % (sys.version, sys.platform))
#
#from django.core import management
#import settings
#management.setup_environ(settings)

import my_django_init
my_django_init.main()

import json
import shoppinglists.views
import inspect

from shoppinglists.api import ShoppingListResource, ShoppingListItemResource, ShoppingListAdapter
from shoppinglists.views import ObjMemberJsonEncoder


import shoppinglists.encoders
shoppinglists.encoders._run_tests()

import shoppinglists.api
shoppinglists.api._run_tests()


#newList = ShoppingList()
#newList.name = 'name ' + str(datetime.now())
#newList.save()
#newItem1 = ShoppingListItem()
#newItem1.shopping_list = newList
#newItem1.name = 'item1 in ' + newList.name
#newItem1.checked = False
#newItem1.save()
#
#adapter = ShoppingListAdapter()
#refreshed_list = ShoppingList.objects.get(pk=newItem1.id)
#resource1 = adapter.adapt_to_resource(refreshed_list)
#jsonData = json.dumps(resource1 , ensure_ascii=False, cls=ObjMemberJsonEncoder)
#print jsonData




#item1 = ShoppingListItemResource()
#item1.name = 'bok choi'
#item1.checked = True
#item2 = ShoppingListItemResource(name = 'bananas', checked=False)
#item2.map['item2'] = 'item2value'
#shopping_list = ShoppingListResource()
#shopping_list.items.append(item1)
#shopping_list.items.append(item2)
#jsonData = json.dumps(shopping_list , ensure_ascii=False, cls=MyJsonEncoder)
#print jsonData

#print '____________ dir'
#d = dir(item1)
#for d1 in d:
#    print d1
#
#print '____________ vars'
#v = vars(item1)
#for v1 in v:
#    print v1
#
#print '____________ mro'
#print ''
#print item1.__class__
#print item1.__class__.__name__
#print type(item1).__name__
#print ''
#mro = inspect.getmro(type(item1))
#for m in mro:
#    print m
#
#print '____________ getmembers'
#for mem in inspect.getmembers(item1):
#    print mem

#members = inspect.getmembers(item1, inspect.ismemberdescriptor())
#members = inspect.getmembers(item1)
#for mem in item1.__dict__.keys():
#    print mem
