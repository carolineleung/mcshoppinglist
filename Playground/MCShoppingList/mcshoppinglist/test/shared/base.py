import logging
from unittest.case import TestCase
import re
from mcshoppinglist.api.constants import ResourceKeys
from mcshoppinglist.shared.logfactory import LogFactory
from mcshoppinglist.shared.mongodb import MongoManager
from mcshoppinglist.shoppinglists.dao import ShoppingListItemDao, ShoppingListDao
from mcshoppinglist.test.shared.httphelpers import HttpTestClientWrapper
from pyramid import testing
from mcshoppinglist.test.shared.mongohelpers import MongoEngineTestHelper

class StaticTestState(object):
    mongo_initialized = False

class ShoppingListTestBase(TestCase):
    """
    Base class for ShoppingList tests.
    """
    def setUp(self):
        self.setUpLogging()
        self.setUpMongoDb()
        self.setUpPyramid()
        
        # TODO Rename to item_dao
        self.itemDao = ShoppingListItemDao()
        # TODO Rename to list_dao
        self.listDao = ShoppingListDao()
        self._id_format_re = re.compile(r'^[a-zA-Z0-9]+$')

    def setUpPyramid(self):
        # Pyramid/pylons testing init.
        # TODO Should we be grabbing these settings from an .ini? (e.g. testing.ini similar to development.ini)
        test_settings = {
            MongoManager.SETTING_MONGODB_PRIMARY_NAME: MongoEngineTestHelper.TEST_MONGODB_NAME,
            MongoManager.SETTING_MONGODB_AUTH_NAME: MongoEngineTestHelper.TEST_MONGODB_NAME,
        }
        self.config = testing.setUp(settings=test_settings)
        testapp = self._create_webtest_testapp(self.config, **test_settings)
        self.http_client = HttpTestClientWrapper(testapp)

    def _create_webtest_testapp(self, global_config, **settings):
        import mcshoppinglist
        app = mcshoppinglist.main(global_config=global_config, **settings)
        from webtest import TestApp
        return TestApp(app)

    def setUpMongoDb(self):
        # Always create a mongo_helper as its used by some of the tests.
        self.mongo_helper = MongoEngineTestHelper()
        # TODO By default recreate the db clean for each tests (no side effects). Move the option to disable db rebuild to config (setup.cfg or development.ini?).
        if not StaticTestState.mongo_initialized:
            # Dropping the database for each test method is very time consuming! (~10x testing time)
            self.mongo_helper.init_mongodb_for_test()
            StaticTestState.mongo_initialized = True

    def setUpLogging(self):
        # TODO Use a logging dict config
#        logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(levelname)s %(message)s')
        # create logger
        logger = LogFactory.get_logger_top()
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)

    def tearDown(self):
        testing.tearDown()

    def _sanitize_json(self, json_data):
        """
        Remove these json fields: "last_modified": "2011-02-17T16:07:28",
        Clean up irrelevant white space e.g.   [ {   "key1":   false,  "key2":   "abc"  }    ]
        """
        new_data = re.sub(r'"last_modified"\s*:\s*"?[0-9T:\-]*"?\s*,?\s*', '', json_data)
        # Remove the irrelevant spaces.
        # This unfortunately also strips matching regex within "quoted,  values".
        # This code should ONLY be used in tests!
        new_data = re.sub(r'([\[\{,]+)\s+(")', r'\1\2', new_data)
        new_data = re.sub(r'\s+([,\]\}])+\s+', r'\1', new_data)
        new_data = re.sub(r'(")\s+(:)\s+', r'\1\2', new_data)
        new_data = re.sub(r'(,)\s+(")', r'\1\2', new_data)
        # Remove the id (they're machine name based in MongoDB so we can't hard code expected ids)
        new_data = re.sub(r'"id"\s*:\s*"?.*"?\s*,?\s*', '', new_data)
        return new_data

    def assertEqualSanitizedJson(self, expected, actual, message=None):
        self.assertEqual(self._sanitize_json(expected), self._sanitize_json(actual), msg=message)

    def create_action_resource(self, which_action, item_resources):
        return {
            ResourceKeys.ACTION_KEY: which_action,
            ResourceKeys.ITEMS_KEY: item_resources
        }

    def is_valid_id_format(self, id):
        return self._id_format_re.match(id)

    def assertIsValidIdFormat(self, id):
        self.assertTrue(self.is_valid_id_format(id))

