from mcshoppinglist.shared.exceptions import ShoppingListError
from mcshoppinglist.shoppinglists.models import ShoppingList

# TODO recreate mongodb per run?
# TODO Move configuration to a file...
class MongoEngineTestHelper(object):
    TEST_MONGODB_NAME = 'mcshoppinglist_test'

    def __init__(self):
        # Tests connect to a test mongodb.
        self.db_name = MongoEngineTestHelper.TEST_MONGODB_NAME

    def drop_database(self):
        js_code = """
        db.dropDatabase();
        """
        try:
            ShoppingList.objects.exec_js(js_code)
        except Exception as ex:
            raise ShoppingListError('Failed to drop test database: {0}'.format(self.db_name), ex)

    def init_mongodb_for_test(self):
        # MongoDB MongoEngine
        import mongoengine
        mongoengine.connect(self.db_name, host='localhost', port=27017)
        # TODO Instead of reconnecting, check that it's connected (from the test base.py calls to MongoManager)
        self.drop_database()

