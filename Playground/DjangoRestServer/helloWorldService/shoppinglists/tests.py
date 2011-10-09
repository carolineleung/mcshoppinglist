"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from datetime import datetime
import httplib
import json
import re
from django.http import  HttpResponse

from django.test import TestCase
from django.test.client import Client
from etags.etagmanager import EtagManager
import models
import shoppinglists
from shoppinglists.api import  ShoppingListAdapter, ShoppingListIndexAdapter, ResourceKeys, ResourceNameConstants, ShoppingListItemAdapter, ActionCrudConstants
from shoppinglists.apierrors import JsonErrorFactory
from shoppinglists.exceptions import  ShoppingListError
from shoppinglists.helpers import JsonHelper
from shoppinglists.models import  ShoppingList, ShoppingListItem, ShoppingListItemDao, ShoppingListDao, ModelStateConstants, EtagCacheEntryDao, EtagCacheEntryDao
from shoppinglists.views import RequestHandlerWrapper


# Running from command line:
# python manage.py test shoppinglists
#
# Running from another script:
# http://docs.djangoproject.com/en/1.2/topics/testing/
# >>> from django.test.utils import setup_test_environment
# >>> setup_test_environment()

#
# http://docs.djangoproject.com/en/1.2/topics/testing/
#

def _drop_database():
    js_code = """
    db.dropDatabase();
    """
    try:
        ShoppingList.objects.exec_js(js_code)
    except Exception as ex:
        msg = 'Failed to drop test database: {0}'.format(db_name)
        print msg
        raise ShoppingListError(msg, ex)

def _init_mongodb_for_test():
    # Tests connect to a different mongodb. TODO recreate mongodb per run.
    # MongoDB MongoEngine
    import mongoengine
    db_name = 'mcshoppinglist_test'
    mongoengine.connect(db_name, host='localhost', port=27017)
    _drop_database()

_init_mongodb_for_test();

# http://docs.python.org/library/datetime.html#strftime-strptime-behavior
# datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
SHARED_DATETIME = datetime(2011, 02, 15, 21, 15, 38)

#class MySmallObj:
#    def __init__(self, name='unknown'):
#        self.name = name
#        self.lastmodified = SHARED_DATETIME
#        self.type = 'MySmallObj'
#
#class MyTestClass:
#    def __init__(self):
#        self.str_var = "str value"
#        self.list_var = ['one', 'two', 'three']
#        self.list_objs_var = [ MySmallObj('obj1'), MySmallObj('obj2'), ]
#        self.dict_var = { 'one': 'val1d', 'two': 'val2d'}
#        self.dic_objs_var = { 'one': MySmallObj('obj1d'), 'two': MySmallObj('obj2d')}
#        self.datetime_var = SHARED_DATETIME
#        self.bool_var = True
#        self.double_var = 1.000888
#        self.decimal_var = decimal.Decimal('1008.0034181451667708')
#        self.type = 'MyTestClass'

class ShoppingListTestDataOneItem:
    def __init__(self):
        # A short test shopping list
        self.newList1 = ShoppingList()
        self.newList1.name = 'Test List Name 1'
        self.newList1.last_modified = SHARED_DATETIME
        dao = ShoppingListDao()
        dao.save(self.newList1)

        self.newItem1 = self.create_and_save_new_item(self.newList1, 'item1 in list: ' + self.newList1.name)

        # A shopping list as resource
        self.shopping_list_resource2 = {
            ResourceKeys.NAME_KEY: 'Test List Name 2 (From Resource)',
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST,
            ResourceKeys.ITEMS_KEY: [
                self.create_item_resource('item1 bok choi'),
                self.create_item_resource('item2 gai lan', True),
                self.create_item_resource('item3 bananas'),
            ]
        }

    def create_item_resource(self, name, checked=False):
        return {
            ResourceKeys.TYPE_KEY: ResourceNameConstants.SHOPPING_LIST_ITEM,
            ResourceKeys.NAME_KEY: name,
            ResourceKeys.CHECKED_KEY: checked,
        }

    def create_and_save_new_item(self, shopping_list, item_name):
        newItem1 = ShoppingListItem()
        newItem1.shopping_list = shopping_list
        newItem1.name = '' + item_name
        newItem1.checked = False
        newItem1.last_modified = SHARED_DATETIME
        dao = ShoppingListItemDao()
        dao.save(newItem1)
        return newItem1

class DaoTest(TestCase):
    def setUp(self):
        self.item_dao = ShoppingListItemDao()
        self.list_dao = ShoppingListDao()

    def _create_list_model(self, list_name='name = test list'):
        list_model = ShoppingList()
        list_model.name = list_name
        self.list_dao.save(list_model)

        refreshed_list_model = self.list_dao.get_by_id(list_model.id)
        self.assertEqual(list_model.id, refreshed_list_model.id)
        self.assertEqual(list_model.name, refreshed_list_model.name)
        return list_model

    def test_list_dao(self):
        self._create_list_model(list_name='name = test_list_dao list')

    def _check_item_model(self, expected_item_model):
        refreshed_item_model = self.item_dao.get_by_id(expected_item_model.id)
        self.assertEqual(expected_item_model.id, refreshed_item_model.id)
        self.assertEqual(expected_item_model.name, refreshed_item_model.name)
        self.assertEqual(expected_item_model.checked, refreshed_item_model.checked)

    def _create_item_model(self, list_model, item_name='name = test item'):
        item_model = ShoppingListItem()
        item_model.name = item_name
        item_model.checked = True
        item_model.shopping_list = list_model

        self.item_dao.save(item_model)
        self._check_item_model(item_model)
        return item_model

    def test_item_dao(self):
        list_model = self._create_list_model(list_name='name = test_item_dao list')
        item_model = self._create_item_model(list_model, item_name='name = test_item_dao item')

        # Update the item
        item_id = item_model.id
        item_model.name += ' updated'
        self.item_dao.save(item_model)
        self._check_item_model(item_model)
        self.assertEqual(item_id, item_model.id)

    def test_etag_dao(self):
        list_model = self._create_list_model(list_name='name = test_etag_dao list')
        item_model = self._create_item_model(list_model, item_name='name = test_etag_dao item')

        etag_manager = EtagManager()
        etag_model = etag_manager.save_etag(item_model)
        etag_dao = EtagCacheEntryDao()
        refreshed_etag_model = etag_dao.get_by_id(etag_model.id)
        self.assertEqual(etag_model.id, refreshed_etag_model.id)
        self.assertEqual(etag_model.etag, refreshed_etag_model.etag)

        refreshed_etag_model = etag_manager.get_etag_model(item_model)
        self.assertIsNotNone(refreshed_etag_model,
                             'refreshed_etag_model was None. '
                             'Failed to retrieve etag for item id: {0}'.format(item_model.id))
        self.assertEqual(etag_model.id, refreshed_etag_model.id)
        self.assertEqual(etag_model.etag, refreshed_etag_model.etag)
        self.assertEqual(str(item_model.id), refreshed_etag_model.target_model_id)

class HttpTestClientWrapper(object):
    # TODO Are these defined somewhere? Don't see them in httlib (py2.7)
    HTTP_METHOD_GET='GET'
    HTTP_METHOD_POST='POST'
    HTTP_METHOD_PUT='PUT'
    HTTP_METHOD_DELETE='DELETE'

    def __init__(self):
        self.client = Client()
        # The URLs with Django client.get() must be relative to the project base (cannot be relative to url patterns in shoppinglists.urls)
        self.base_uri = '/api/v1/shoppinglists/'

    def _print_request_info(self, request_uri, http_method, request_body=None, etag_header=None):
        print '\n__________ REQUEST:\n'
        print '\n{0} {1}\n'.format(http_method, request_uri)
        if etag_header:
            print 'If-None-Match: {0}\n'.format(etag_header)
        if request_body:
            print '{0}\n'.format(request_body)

    def _print_response_info(self, response):
        print '__________ RESPONSE:  {0}\n'.format(response.status_code)
        try:
            json_obj = json.loads(response.content)
            pretty_json = json.dumps(json_obj, sort_keys=True, indent=4)
            print '{0}\n\n'.format(pretty_json)
        except Exception:
            print '{0}\n\n'.format(response.content)

    def create_relative_uri(self, uri_suffix=''):
        return '{0}{1}'.format(self.base_uri, uri_suffix)

    def _make_http_request_rel_uri(self, relative_uri, expected_status_code,
                                   http_method, request_body=None, etag_header=None):
        request_uri = self.create_relative_uri(relative_uri)
        self._print_request_info(request_uri, http_method, request_body, etag_header)
        if http_method == HttpTestClientWrapper.HTTP_METHOD_GET:
            if etag_header:
                # If-None-Match must be caps w/ underscores in Django
                quoted_etag = '"{0}"'.format(etag_header)
                response = self.client.get(request_uri, data={}, follow=False, HTTP_IF_NONE_MATCH=quoted_etag)
            else:
                response = self.client.get(request_uri)
        elif http_method == HttpTestClientWrapper.HTTP_METHOD_POST:
            response = self.client.post(request_uri, request_body, content_type=JsonHelper.JSON_CONTENT_TYPE)
        elif http_method == HttpTestClientWrapper.HTTP_METHOD_PUT:
            response = self.client.put(request_uri, request_body, content_type=JsonHelper.JSON_CONTENT_TYPE)
        else:
            raise Exception('Unimplemented method {0}'.format(http_method))

        self._print_response_info(response)
        if response.status_code != expected_status_code:
            raise Exception('Expected status code: {0}   Actual: {1}'.format(expected_status_code, response.status_code))
        return response

    def get_rel_uri(self, relative_uri, expected_status_code, etag_header=None):
        """
        Make a get request to a URI relative to the API at /api/v1/shoppinglists/
        """
        return self._make_http_request_rel_uri(relative_uri, expected_status_code,
                                               HttpTestClientWrapper.HTTP_METHOD_GET, etag_header=etag_header)

    def put_rel_uri(self, relative_uri, expected_status_code, request_body):
        return self._make_http_request_rel_uri(relative_uri, expected_status_code,
                                               HttpTestClientWrapper.HTTP_METHOD_PUT, request_body)

    def post_rel_uri(self, relative_uri, expected_status_code, request_body):
        return self._make_http_request_rel_uri(relative_uri, expected_status_code,
                                               HttpTestClientWrapper.HTTP_METHOD_POST, request_body)

class ShoppingListTestBase(TestCase):
    def setUp(self):
        self.itemDao = ShoppingListItemDao()
        self.listDao = ShoppingListDao()
        self.client = Client()
        self.http_client = HttpTestClientWrapper()
        self._id_format_re = re.compile(r'^[a-zA-Z0-9]+$')

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
        return self._id_format_re.match(id) != None

    def assertIsValidIdFormat(self, id):
        self.assertTrue(self.is_valid_id_format(id))

class AdaptersTest(ShoppingListTestBase):
    def setUp(self):
        super(AdaptersTest, self).setUp()
        self.test_data = ShoppingListTestDataOneItem()

    def test_shopping_list_adapter(self):
        adapter = ShoppingListAdapter()
        refreshed_list = self.listDao.get_by_id(self.test_data.newList1.id)
        resource1 = adapter.adapt_to_resource(refreshed_list)
        #print 'Adapted to resource: ' + str(resource1)
        if resource1[ResourceKeys.LAST_MODIFIED_KEY] != self.test_data.newList1.last_modified \
            or len(resource1[ResourceKeys.ITEMS_KEY]) != 1 \
            or resource1[ResourceKeys.NAME_KEY] != self.test_data.newList1.name \
            or resource1[ResourceKeys.ITEMS_KEY][0][ResourceKeys.NAME_KEY] != self.test_data.newItem1.name:
            raise Exception('Failed to adapt model to resource.')

    def test_shopping_list_index_adapter(self):
        # PRE: At least one ShoppingList saved, i.e. len(ShoppingList.objects) > 0
        adapter = ShoppingListIndexAdapter()
        resource = adapter.adapt_to_resource()
        if not resource\
            or len(resource) <= 0:
            raise Exception('Failed to get shopping list index.')
        self.assertIsValidIdFormat(resource[ResourceKeys.ENTRIES_KEY][0][ResourceKeys.ID_KEY])
        # TODO More checks

    def test_update_list_from_full_resource(self):
        adapter = ShoppingListAdapter()
        expected_resource = self.test_data.shopping_list_resource2
        # Update the already persisted list using the in memory (not yet persisted) resource dict
        expected_resource[ResourceKeys.ID_KEY] = self.test_data.newList1.id
        updated_list_model = adapter.update_from_resource(
            self.test_data.newList1.id, self.test_data.shopping_list_resource2)
        self.assertEqual(expected_resource[ResourceKeys.NAME_KEY], updated_list_model.name)
        updated_items_queryset = self.itemDao.get_by_shopping_list_model(updated_list_model)
        # Check that new items were created (and old deleted).
        # The combination of checking count and each item name guarantees this.
        self.assertEqual(len(expected_resource[ResourceKeys.ITEMS_KEY]), updated_items_queryset.count())
        self.assertTrue(updated_items_queryset.count() > 0)
        for updated_item in updated_items_queryset:
            found = False
            for expected_item in expected_resource[ResourceKeys.ITEMS_KEY]:
                if expected_item[ResourceKeys.NAME_KEY] == updated_item.name:
                    # Can't check id because our expected resources were not yet persisted.
                    found = True
                    # TODO Additional checks
                    break
            self.assertTrue(found)
        # Cannot check old item deleted due to sqlite reusing the id... (is it b/c it's in memory sqlite? or because the Django test harness runs within a transaction?)
        # Check all old items deleted
        #deleted_item = ShoppingListItem.objects.get(pk=self.test_data.newItem1.id)
        #self.assertEquals(None, deleted_item)

    def test_update_item_from_full_resource(self):
        adapter = ShoppingListItemAdapter()
        resource = adapter.adapt_to_resource(self.test_data.newItem1)
        expected_name = resource[ResourceKeys.NAME_KEY] + ' Updated!'
        resource[ResourceKeys.NAME_KEY] = expected_name
        expected_checked = not resource[ResourceKeys.CHECKED_KEY]
        resource[ResourceKeys.CHECKED_KEY] = expected_checked
        adapter.update_from_resource(resource)
        updatedItem1 = self.itemDao.get_by_id(self.test_data.newItem1.id)
        self.assertEqual(expected_checked, updatedItem1.checked)
        self.assertEqual(expected_name, updatedItem1.name)
        self.assertNotEquals(self.test_data.newItem1.last_modified, updatedItem1.last_modified)

    def test_update_item_checked_from_partial_resource(self):
        adapter = ShoppingListItemAdapter()
        resource = adapter.adapt_to_resource(self.test_data.newItem1)
        allowed_keys = [ ResourceKeys.ID_KEY, ResourceKeys.CHECKED_KEY ]
        # Remove everything except id and checked
        for key in resource.keys():
            if key not in allowed_keys:
                del resource[key]
        expected_checked = not resource[ResourceKeys.CHECKED_KEY]
        resource[ResourceKeys.CHECKED_KEY] = expected_checked
        adapter.update_from_resource(resource)
        updatedItem1 = self.itemDao.get_by_id(self.test_data.newItem1.id)
        # Checked must be updated
        self.assertEqual(expected_checked, updatedItem1.checked)
        # Ensure nothing else important changed
        self.assertEqual(self.test_data.newItem1.name, updatedItem1.name)
        self.assertEqual(self.test_data.newItem1.shopping_list, updatedItem1.shopping_list)
        self.assertNotEquals(self.test_data.newItem1.last_modified, updatedItem1.last_modified)


def _create_relative_uri(uri_suffix = ''):
    """
    The URLs with client.get() must be relative to the project base (cannot be relative to url patterns in shoppinglists.urls)
    """
    return '{0}{1}'.format('/api/v1/shoppinglists/', uri_suffix)

def _print_test_rr_info(message, uri, json_data, method='POST'):
    try:
        json_obj = json.loads(json_data)
        pretty_json = json.dumps(json_obj, sort_keys=True, indent=4)
        print('{0}:\n{1}\n{2}\n{3}\n//_____________________________\n\n'.format(message, method, uri, pretty_json))
    except Exception:
        print('Failed to print test info.')

# TODO These tests are brittle because the expected responses (JSON payloads) are hard coded below.
class ShoppingListViewTest(ShoppingListTestBase):

    def setUp(self):
        super(ShoppingListViewTest, self).setUp()
        self.test_data = ShoppingListTestDataOneItem()

    def test_create_shopping_list(self):
        json_post_data = JsonHelper.serialize_to_json(self.test_data.shopping_list_resource2)
        response_from_post = self.http_client.post_rel_uri('', httplib.CREATED, json_post_data)
        expected = '{ "type": "ShoppingList", "id": 2, "name": "Test List Name 2 (From Resource)"}'
        # Use _remove_last_modified to circumvent datetime.now() variance.
        self.assertEqualSanitizedJson(expected, response_from_post.content)

        list_resource = JsonHelper.deserialize_from_json(response_from_post.content)
        # TODO Assert Location header was returned and points to new resource.
        response_from_get = self.http_client.get_rel_uri(
            '{0}/'.format(list_resource[ResourceKeys.ID_KEY]), httplib.OK)
        expected = '{"items": [{"checked": false, "name": "item1 bok choi", "labels": "",  "type": "ShoppingListItem", "id": 2}, {"checked": true, "name": "item2 gai lan", "labels": "",  "type": "ShoppingListItem", "id": 3}, {"checked": false, "name": "item3 bananas", "labels": "",  "type": "ShoppingListItem", "id": 4}],  "type": "ShoppingList", "id": 2, "name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response_from_get.content)

    def test_get_shopping_list_index(self):
        _drop_database()
        self.test_data = ShoppingListTestDataOneItem()
        response = self.http_client.get_rel_uri('', httplib.OK)
        expected = '{"count": 1, "type": "ShoppingListIndex", "entries": [{"type": "ShoppingListIndexEntry", "id": 1}]}'
        self.assertEqualSanitizedJson(expected, response.content)

    def test_get_shopping_list_detail(self):
        # Add some labels
        self.test_data.newItem1.labels = "label1,label2,label3"
        self.itemDao.save(self.test_data.newItem1)
        response = self.http_client.get_rel_uri('{0}/'.format(models.get_id_str(self.test_data.newList1)), httplib.OK)
        expected = '{"items": [{"checked": false, "name": "item1 in list: Test List Name 1", "labels": "label1,label2,label3", "last_modified": "2011-02-15T21:15:38", "type": "ShoppingListItem", "id": 1}], "last_modified": "2011-02-15T21:15:38", "type": "ShoppingList", "id": 1, "name": "Test List Name 1"}'
        self.assertEqualSanitizedJson(expected, response.content)
        response_snap = EtagResponseDataSnapshot(response, self)

    def test_update_item_checked(self):
        refreshed_item_model = self.itemDao.get_by_id(self.test_data.newItem1.id)
        post_resource = self.create_action_resource(ActionCrudConstants.UPDATE,
            [ { ResourceKeys.ID_KEY: models.get_id_str(refreshed_item_model),
                ResourceKeys.CHECKED_KEY: (not refreshed_item_model.checked)
                }])
        json_post_data = JsonHelper.serialize_to_json(post_resource)
        response = self.http_client.post_rel_uri(
            '{0}/items/'.format(models.get_id_str(self.test_data.newList1)), httplib.OK, json_post_data)
        expected = '{"items": [{"checked": true, "name": "item1 in list: Test List Name 1", "labels": "",  "type": "ShoppingListItem", "id": 1}], "update_count": 1}'
        self.assertEqualSanitizedJson(expected, response.content)

    def test_update_shopping_list_full_replace(self):
        expected_resource = self.test_data.shopping_list_resource2
        # Update the already persisted list using the test's in memory (not yet persisted) resource dict
        newList1_id = models.get_id_str(self.test_data.newList1)
        expected_resource[ResourceKeys.ID_KEY] = newList1_id
        json_post_data = JsonHelper.serialize_to_json(expected_resource )
        rel_uri = '{0}/'.format(newList1_id);
        response = self.http_client.put_rel_uri(rel_uri, httplib.OK, json_post_data)
        expected = '{"items": [{"checked": false,"name": "item1 bok choi","labels": "","type": "ShoppingListItem","id": 2}, {"checked": true,"name": "item2 gai lan","labels": "","type": "ShoppingListItem","id": 3}, {"checked": false,"name": "item3 bananas","labels": "","type": "ShoppingListItem","id": 4}],"type": "ShoppingList","id": 1,"name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.content)
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        expected = '{"items": [{"checked": false,"name": "item1 bok choi","labels": "","type": "ShoppingListItem","id": 2}, {"checked": true,"name": "item2 gai lan","labels": "","type": "ShoppingListItem","id": 3}, {"checked": false,"name": "item3 bananas","labels": "","type": "ShoppingListItem","id": 4}],"type": "ShoppingList","id": 1,"name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.content) # 'Expected list meta and items to be replaced.'
        expected_item1_name = expected_resource[ResourceKeys.ITEMS_KEY][0][ResourceKeys.NAME_KEY]
        self.assertTrue(response.content.find(expected_item1_name) >= 0)

    def test_update_shopping_list_meta(self):
        expected_resource = self.test_data.shopping_list_resource2
        # Update the already persisted list using the test's in memory (not yet persisted) resource dict
        newList1_id = models.get_id_str(self.test_data.newList1)
        expected_resource[ResourceKeys.ID_KEY] = newList1_id
        json_post_data = JsonHelper.serialize_to_json(expected_resource )
        rel_uri = '{0}/meta/'.format(newList1_id);
        response = self.http_client.put_rel_uri(rel_uri, httplib.OK, json_post_data)
        expected = '{"last_modified": "2011-03-09T19:48:21", "type": "ShoppingList", "id": 1, "name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.content)
        # Check getting updated meta.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        expected = '{"type": "ShoppingList","id": 1,"name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.content) # 'Expected list meta to be replaced, but items unchanged.'
        self.assertTrue(response.content.find('"{0}":'.format(ResourceKeys.ITEMS_KEY)) < 0)
        # Get the full list and ensure we didn't delete the items.
        rel_uri = '{0}/'.format(newList1_id)
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        expected = '{"items": [{"checked": false,"name": "item1 in list: Test List Name 1","labels": "","type": "ShoppingListItem","id": 1}],"type": "ShoppingList","id": 1,"name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.content)

    def test_create_new_items(self):
        # Create in memory items
        item1_resource = self.test_data.create_item_resource('kei zi')
        item2_resource = self.test_data.create_item_resource('ngai gwa')
        item2_resource['checked'] = True
        item2_resource['id'] = -1
        action_resource = self.create_action_resource(ActionCrudConstants.CREATE,
            [ item1_resource, item2_resource ])

        json_post_data = JsonHelper.serialize_to_json(action_resource)
        newList1_id = models.get_id_str(self.test_data.newList1)
        # POST to create them.
        response = self.http_client.post_rel_uri(
            '{0}/items/'.format(newList1_id), httplib.CREATED, json_post_data)
        expected = '[{"checked": false, "name": "kei zi", "labels": "",  "type": "ShoppingListItem", "id": 2}, {"checked": true, "name": "ngai gwa", "labels": "",  "type": "ShoppingListItem", "id": 3}]'
        # Use _remove_last_modified to circumvent datetime.now() variance.
        self.assertEqualSanitizedJson(expected, response.content)

        # Assert in db
        actual_items_array = JsonHelper.deserialize_from_json(response.content)
        item1_model = self.itemDao.get_by_id(actual_items_array[0]['id'])
        self.assertIsNotNone(item1_model)
        self.assertEqual(item1_resource['name'], item1_model.name)
        item2_model = self.itemDao.get_by_id(actual_items_array[1]['id'])
        self.assertEqual(item2_resource['name'], item2_model.name)

    def test_delete_items(self):
        # Create a second and third item so the first item isn't lonely.
        newItem2 = self.test_data.create_and_save_new_item(self.test_data.newList1, 'item2')
        newItem3 = self.test_data.create_and_save_new_item(self.test_data.newList1, 'item3')

        # Sanity check that the model exists
        self.assertIsNotNone(self.itemDao.get_by_id(self.test_data.newItem1.id))

        # Delete the first item
        newItem1_id = models.get_id_str(self.test_data.newItem1)
        action_resource = self.create_action_resource( ActionCrudConstants.DELETE,
            [{ ResourceKeys.ID_KEY: newItem1_id }] )
        json_post_data = JsonHelper.serialize_to_json( action_resource )
        newList1_id = models.get_id_str(self.test_data.newList1)
        # DELETE
        response = self.http_client.post_rel_uri(
            '{0}/items/'.format(newList1_id), httplib.OK, json_post_data)
        self.assertEqual('', response.content)
        deleted_model1 = self.itemDao.get_by_id(self.test_data.newItem1.id)
        self.assertEqual(ModelStateConstants.DELETED, deleted_model1.state)

        # Get the list and check that our other items are there, but the deleted item is not.
        response = self.http_client.get_rel_uri('{0}/'.format(newList1_id), httplib.OK)
        resp_resource = JsonHelper.deserialize_from_json(response.content)
        found_item_ids = set([item_r[ResourceKeys.ID_KEY] for item_r in resp_resource[ResourceKeys.ITEMS_KEY]])
        self.assertTrue(not newItem1_id in found_item_ids)
        newItem2_id = models.get_id_str(newItem2)
        self.assertTrue(newItem2_id in found_item_ids)
        newItem3_id = models.get_id_str(newItem3)
        self.assertTrue(newItem3_id in found_item_ids)

        # Delete item2 and item3 in same request.
        action_resource = self.create_action_resource( ActionCrudConstants.DELETE,
            [{ ResourceKeys.ID_KEY: newItem2_id },
             { ResourceKeys.ID_KEY: newItem3_id }] )
        json_post_data = JsonHelper.serialize_to_json( action_resource )
        # DELETE
        response = self.http_client.post_rel_uri(
            '{0}/items/'.format(newList1_id), httplib.OK, json_post_data)
        self.assertEqual('', response.content)
        deleted_model2 = self.itemDao.get_by_id(newItem2_id)
        self.assertEqual(ModelStateConstants.DELETED, deleted_model2.state)
        deleted_model3 = self.itemDao.get_by_id(newItem3_id)
        self.assertEqual(ModelStateConstants.DELETED, deleted_model3.state)


class ShoppingListViewNoDataTest(ShoppingListTestBase):
    def setUp(self):
        super(ShoppingListViewNoDataTest, self).setUp()
        # Do not create any expected data (lists, items).

    def test_get_empty_shopping_list_index(self):
        _drop_database()
        dao = ShoppingListDao()
        self.assertEqual(0, dao.get_count(), 'PRE: no shopping lists.')

        response = self.http_client.get_rel_uri('', httplib.OK)
        expected = '{"count": 0, "type": "ShoppingListIndex", "entries": []}'
        self.assertEqual(expected, response.content)

class EtagResponseDataSnapshot(object):
    def __init__(self, response, test_case):
        self.asserter = test_case

        # TODO Are the HTTP headers constants ETag etc. defined somewhere? http://docs.python.org/library/httplib.html
        self.etag = response['ETag']
        self.asserter.assertTrue(len(self.etag) > 0)
        print 'ETag: {0}'.format(self.etag)

        self.last_modified = response['Last-Modified']
        self.asserter.assertTrue(len(self.last_modified) > 0)

        self.response = response

# TODO Add test for if we just change the shopping list model, not the item
# TODO Add tests for multiple items changing
class ShoppingListViewDiffTest(ShoppingListTestBase):
    def setUp(self):
        super(ShoppingListViewDiffTest, self).setUp()
        self.test_data = ShoppingListTestDataOneItem()

    def test_get_shopping_list_diff_full_no_etag(self):
        self.http_client.get_rel_uri(
            '{0}/diff/'.format(self.test_data.newList1.id), httplib.OK)
        # TODO assert response.content

    def test_get_shopping_list_diff_invalid_etag(self):
        self.http_client.get_rel_uri(
            '{0}/diff/'.format(self.test_data.newList1.id), httplib.OK, etag_header='INVALID_ETAG')
        # TODO assert response.content

    def test_get_shopping_list_diff(self):
        rel_uri = '{0}/diff/'.format(self.test_data.newList1.id)
        # With no conditional GET (no If-Modified-Since/If-None-Match), expect the full list and an etag.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        response_snap1 = EtagResponseDataSnapshot(response, self)
        # TODO assert response.content

        # Check for 304 not modified
        response = self.http_client.get_rel_uri(rel_uri, httplib.NOT_MODIFIED, etag_header=response_snap1.etag)
        self.assertEqual('', response.content)

        # Check for same shopping list items when we include an invalid ETag.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header='INVALID_ETAG')
        self.assertEqual(response_snap1.response.content, response.content)

        # Update the item model
        self.test_data.newItem1.name += ' updated'
        self.itemDao.save(self.test_data.newItem1)

        # Check that we get the updated item
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header=response_snap1.etag)
        response_snap2 = EtagResponseDataSnapshot(response, self)
        self.assertNotEqual(response_snap1.etag, response_snap2.etag,
            'The ETag must change after the ShoppingListItem is updated.')
        self.assertNotEqual(response_snap1.last_modified, response_snap2.last_modified,
            'The Last-Modified must change after the ShoppingListItem is updated.')
        # TODO Assert last modified greater than before
        # TODO Assert content includes item updated
        self.assertTrue(response.content.find(self.test_data.newItem1.name) >= 0)

        # Check for 304 not modified, with the new etag
        response = self.http_client.get_rel_uri(rel_uri, httplib.NOT_MODIFIED, etag_header=response_snap2.etag)
        self.assertEqual('', response.content)

        # Add a new item
        newItem2 = self.test_data.create_and_save_new_item(self.test_data.newList1, 'granola')

        # Check that we get only the new item using the old etag
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header=response_snap2.etag)
        response_snap3 = EtagResponseDataSnapshot(response, self)
        # TODO Better asserts for content
        self.assertTrue(response.content.find(self.test_data.newItem1.name) < 0)
        self.assertTrue(response.content.find(newItem2.name) >= 0)

        # Check that we get a 304 now for the new item
        response = self.http_client.get_rel_uri(rel_uri, httplib.NOT_MODIFIED, etag_header=response_snap3.etag)
        self.assertEqual(0, len(response.content))

        # Update both items
        self.test_data.newItem1.name += ' again'
        self.itemDao.save(self.test_data.newItem1)
        newItem2.name += ' updated'
        self.itemDao.save(newItem2)

        # Ensure both updated items are returned
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header=response_snap3.etag)
        #response_snap4 = ResponseDataSnapshot(response, self)
        # TODO Better asserts re. content
        self.assertTrue(response.content.find(self.test_data.newItem1.name) >= 0)
        self.assertTrue(response.content.find(newItem2.name) >= 0)

    def test_get_shopping_list_diff_deleted(self):
        # Create a second and third item so the first item isn't lonely.
        newItem2 = self.test_data.create_and_save_new_item(self.test_data.newList1, 'item2')
        newItem3 = self.test_data.create_and_save_new_item(self.test_data.newList1, 'item3')

        rel_uri = '{0}/diff/'.format(self.test_data.newList1.id)
        # With no conditional GET (no If-Modified-Since/If-None-Match), expect the full list and an etag.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        # TODO assert response.content
        response_snap1 = EtagResponseDataSnapshot(response, self)

        # Delete the first item
        self.itemDao.delete(self.test_data.newItem1)

        # Get the diff, expect item marked deleted
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header=response_snap1.etag)
        #response_snap2 = ResponseDataSnapshot(response, self)
        response_resource2 = JsonHelper.deserialize_from_json(response.content)
        items_resource2 = response_resource2['items']
        self.assertEqual(1, len(items_resource2), msg='Expected diff to show deleted item.')
        self.assertEqual(models.get_id_str(self.test_data.newItem1), items_resource2[0][ResourceKeys.ID_KEY])
        self.assertEqual(ModelStateConstants.DELETED, items_resource2[0][ResourceKeys.STATE_KEY])

        # Get the full list (no etag), expect the deleted item to be present.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        self.assertTrue(response.content.find('"id": "{0}"'.format(models.get_id_str(self.test_data.newItem1))) >= 0)
        # TODO assert id 1 state == DELETED
        self.assertTrue(response.content.find('"id": "{0}"'.format(models.get_id_str(newItem2))) >= 0)
        self.assertTrue(response.content.find('"id": "{0}"'.format(models.get_id_str(newItem3))) >= 0)

        # TODO Additional tests: delete more items, check again.

class RequestHandlerWrapperTest(TestCase):
    EXPECTED_VALUE = 42

    @staticmethod
    def _fake_handler_static():
        return RequestHandlerWrapperTest.EXPECTED_VALUE

    def _fake_handler_instance(self):
        return RequestHandlerWrapperTest.EXPECTED_VALUE

    def _fake_handler_instance_args(self, arg1, arg2):
        self.assertEqual('arg1value', arg1)
        self.assertEqual('arg2value', arg2)
        return RequestHandlerWrapperTest.EXPECTED_VALUE

    def _fake_handler_raise(self):
        raise Exception('Expected this error.')

    def _fake_handler_raise_with_traceback(self):
        try:
            raise ShoppingListError('Expected this error with traceback 1.')
        except Exception as ex:
            raise ShoppingListError('Expected this error 2.', ex)

    def test_wrapper(self):
        actual_value = RequestHandlerWrapper.handle(RequestHandlerWrapperTest._fake_handler_static)
        self.assertEqual(RequestHandlerWrapperTest.EXPECTED_VALUE, actual_value)
        actual_value = RequestHandlerWrapper.handle(self._fake_handler_instance)
        self.assertEqual(RequestHandlerWrapperTest.EXPECTED_VALUE, actual_value)
        actual_value = RequestHandlerWrapper.handle(self._fake_handler_instance_args, 'arg1value', 'arg2value')
        self.assertEqual(RequestHandlerWrapperTest.EXPECTED_VALUE, actual_value)

    def test_wrapper_exceptions(self):
        actual_value = RequestHandlerWrapper.handle(self._fake_handler_raise)
        self.assertTrue(issubclass(actual_value.__class__, HttpResponse))
        json_obj_dict = JsonHelper.deserialize_from_json(actual_value.content)
        self.assertTrue(JsonErrorFactory.MESSAGE_KEY in json_obj_dict)
        self.assertTrue(JsonErrorFactory.CODE_KEY in json_obj_dict)

    def test_wrapper_exceptions(self):
        actual_value = RequestHandlerWrapper.handle(self._fake_handler_raise_with_traceback)
        self.assertTrue(issubclass(actual_value.__class__, HttpResponse))
        print(actual_value.content)
        json_obj_dict = JsonHelper.deserialize_from_json(actual_value.content)
        self.assertTrue(JsonErrorFactory.MESSAGE_KEY in json_obj_dict)
        self.assertTrue(JsonErrorFactory.CODE_KEY in json_obj_dict)
        trace_deep = json_obj_dict[JsonErrorFactory.TRACE_DEEP_KEY]
        self.assertTrue(trace_deep.lower().find('file') >= 0, 'Missing traceback.')
        trace_shallow = json_obj_dict[JsonErrorFactory.TRACE_SHALLOW_KEY]
        self.assertTrue(trace_shallow.lower().find('file') >= 0, 'Missing traceback.')

class ShoppingListExceptionTest(TestCase):
    EXPECTED_MESSAGE1 = 'Expected message 1'
    EXPECTED_MESSAGE2 = 'Expected message 2'
    EXPECTED_MESSAGE3 = 'Expected message 3'

    def test_message(self):
        try:
            raise ShoppingListError(ShoppingListExceptionTest.EXPECTED_MESSAGE1)
        except Exception as ex:
            self.assertEquals(ShoppingListExceptionTest.EXPECTED_MESSAGE1, ex.message)

    def test_rethrow(self):
        try:
            try:
                try:
                    raise ShoppingListError(ShoppingListExceptionTest.EXPECTED_MESSAGE1)
                except Exception as ex3:
                    raise ShoppingListError(ShoppingListExceptionTest.EXPECTED_MESSAGE2, ex3)
            except Exception as ex2:
                raise ShoppingListError(ShoppingListExceptionTest.EXPECTED_MESSAGE3, ex2)
        except ShoppingListError as ex:
            self.assertEquals(ShoppingListExceptionTest.EXPECTED_MESSAGE3, ex.message)
            self.assertEquals(ShoppingListExceptionTest.EXPECTED_MESSAGE2, ex.inner_exception.message)
            self.assertEquals(ShoppingListExceptionTest.EXPECTED_MESSAGE1, ex.inner_exception.inner_exception.message)
            print ex.traceback_str
            self.assertTrue(len(ex.traceback_str) > 0)

#class TypeResolverTest(TestCase):
#    def test_shopping_list_resolver(self):
#        resolver = ShoppingListTypeResolver()
#        type_name = 'ShoppingListIndexResource'
#        actual_type = resolver.resolve(type_name)
#        # issubclass(actual_type, classobj) # classobj cannot be found
#        self.assertEqual(type(actual_type).__name__, 'classobj')
#        self.assertEqual(type_name, actual_type.__name__)



# TODO This should be alongside the EtagManager :(
class EtagManagerTest(TestCase):
    def setUp(self):
        self.etag_manager = EtagManager()
        self.test_data = ShoppingListTestDataOneItem()

    def test_generate_etag(self):
        model = self.test_data.newList1
        etag = self.etag_manager.generate_etag(model, model.last_modified)
        print('etag: {0}'.format(etag))
        #self.assertTrue(etag.contains('ShoppingList:1'))
        self.etag_manager.save_etag(model, model.last_modified)
        check_etag = self.etag_manager.get_etag_model(model).etag
        print('check_etag: {0}'.format(check_etag))
        #self.assertEqual(etag, check_etag)
        last_modified = self.etag_manager.get_last_modified_from_etag(check_etag)
        print('last_modified: {0}'.format(last_modified))
        self.assertEqual(model.last_modified, last_modified)

