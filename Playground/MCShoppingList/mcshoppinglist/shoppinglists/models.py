from mongoengine.document import Document
from mongoengine.fields import  StringField, DateTimeField, ReferenceField, BooleanField
from mcshoppinglist.shared.models.constants import DEFAULT_DATE, DEFAULT_STATE

class ShoppingList(Document):
    # id = None # TODO Try id = None so that IDE syntax highlighting thinks there's an id on this. (Will adding id = None break MongoEngine?)
    name = StringField(max_length=200)
    last_modified = DateTimeField(default=DEFAULT_DATE)
    state = StringField(max_length=10, min_length=1, default=DEFAULT_STATE)

    def __str__(self):
        # http://stackoverflow.com/questions/1307014/python-str-versus-unicode
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'name: {0}, id: {1}'.format(self.name, self.id)

class ShoppingListItem(Document):
    # TODO Revise to use id instead?
    shopping_list = ReferenceField(ShoppingList)
    name = StringField(max_length=200, default='')
    checked = BooleanField(default=False)
    last_modified = DateTimeField(default=DEFAULT_DATE)
    labels = StringField(max_length=300, default='')
    state = StringField(max_length=10, min_length=1, default=DEFAULT_STATE)

    def __str__(self):
        # http://stackoverflow.com/questions/1307014/python-str-versus-unicode
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'name: {0}, id: {1}'.format(self.name, self.id)

