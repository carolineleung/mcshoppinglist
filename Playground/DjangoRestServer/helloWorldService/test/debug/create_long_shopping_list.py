import my_django_init
my_django_init.main()
from datetime import datetime
import random
from shoppinglists.models import ShoppingListItem, ShoppingList

def main():
    SHARED_DATETIME = datetime(2011, 02, 15, 21, 15, 38)
    newList = ShoppingList()
    newList.name = 'Test List Name %s' % SHARED_DATETIME
    newList.save()
    print('Created shopping list id: %s' % newList.id)

    count = 0
    while count < 15:
        count += 1
        newItem1 = ShoppingListItem()
        newItem1.shopping_list = newList
        newItem1.name = 'item #' + str(count)
        newItem1.checked = bool(random.randint(0, 1))
        
        newItem1.save()
        print('Created item id: %s : %s' % (newItem1.id, newItem1.name))

if __name__ == "__main__":
#    count = 0
#    while count < 20:
#        main()
#        count+=1
    main()
