import httplib
from mcshoppinglist.api.constants import ActionCrudConstants, ResourceKeys
from mcshoppinglist.shared.helpers import  JsonHelper
from mcshoppinglist.shared.models.constants import ModelStateConstants
from mcshoppinglist.shared.models.helpers import get_id_str
from mcshoppinglist.test.shared.base import ShoppingListTestBase
from mcshoppinglist.test.shared.httphelpers import EtagResponseDataSnapshot
from mcshoppinglist.test.shared.shoppinglisttestdata import ShoppingListTestDataOneItem



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
        self.assertEqualSanitizedJson(expected, response_from_post.body)

        list_resource = JsonHelper.deserialize_from_json(response_from_post.body)
        # TODO Assert Location header was returned and points to new resource.
        response_from_get = self.http_client.get_rel_uri(
            '{0}/'.format(list_resource[ResourceKeys.ID_KEY]), httplib.OK)
        expected = '{"items": [{"checked": false, "name": "item1 bok choi", "labels": "",  "type": "ShoppingListItem", "id": 2}, {"checked": true, "name": "item2 gai lan", "labels": "",  "type": "ShoppingListItem", "id": 3}, {"checked": false, "name": "item3 bananas", "labels": "",  "type": "ShoppingListItem", "id": 4}],  "type": "ShoppingList", "id": 2, "name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response_from_get.body)

    def test_get_shopping_list_index(self):
        # Ensure there's nothing in the db
        self.mongo_helper.drop_database()
        self.test_data = ShoppingListTestDataOneItem()
        response = self.http_client.get_rel_uri('', httplib.OK)
        expected = '{"count": 1, "type": "ShoppingListIndex", "entries": [{"type": "ShoppingListIndexEntry", "id": 1}]}'
        self.assertEqualSanitizedJson(expected, response.body)

    def test_get_shopping_list_detail(self):
        # Add some labels
        self.test_data.newItem1.labels = "label1,label2,label3"
        self.itemDao.save(self.test_data.newItem1)
        response = self.http_client.get_rel_uri('{0}/'.format(get_id_str(self.test_data.newList1)), httplib.OK)
        expected = '{"items": [{"checked": false, "name": "item1 in list: Test List Name 1", "labels": "label1,label2,label3", "last_modified": "2011-02-15T21:15:38", "type": "ShoppingListItem", "id": 1}], "last_modified": "2011-02-15T21:15:38", "type": "ShoppingList", "id": 1, "name": "Test List Name 1"}'
        self.assertEqualSanitizedJson(expected, response.body)
        # Using EtagResponseDataSnapshot for its asserts
        EtagResponseDataSnapshot(response, self)

    def test_update_item_checked(self):
        refreshed_item_model = self.itemDao.get_by_id(self.test_data.newItem1.id)
        post_resource = self.create_action_resource(ActionCrudConstants.UPDATE,
            [ { ResourceKeys.ID_KEY: get_id_str(refreshed_item_model),
                ResourceKeys.CHECKED_KEY: (not refreshed_item_model.checked)
                }])
        json_post_data = JsonHelper.serialize_to_json(post_resource)
        response = self.http_client.post_rel_uri(
            '{0}/items/'.format(get_id_str(self.test_data.newList1)), httplib.OK, json_post_data)
        expected = '{"items": [{"checked": true, "name": "item1 in list: Test List Name 1", "labels": "",  "type": "ShoppingListItem", "id": 1}], "update_count": 1}'
        self.assertEqualSanitizedJson(expected, response.body)

    def test_update_shopping_list_full_replace(self):
        expected_resource = self.test_data.shopping_list_resource2
        # Update the already persisted list using the test's in memory (not yet persisted) resource dict
        newList1_id = get_id_str(self.test_data.newList1)
        expected_resource[ResourceKeys.ID_KEY] = newList1_id
        json_post_data = JsonHelper.serialize_to_json(expected_resource )
        rel_uri = '{0}/'.format(newList1_id)
        response = self.http_client.put_rel_uri(rel_uri, httplib.OK, json_post_data)
        expected = '{"items": [{"checked": false,"name": "item1 bok choi","labels": "","type": "ShoppingListItem","id": 2}, {"checked": true,"name": "item2 gai lan","labels": "","type": "ShoppingListItem","id": 3}, {"checked": false,"name": "item3 bananas","labels": "","type": "ShoppingListItem","id": 4}],"type": "ShoppingList","id": 1,"name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.body)
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        expected = '{"items": [{"checked": false,"name": "item1 bok choi","labels": "","type": "ShoppingListItem","id": 2}, {"checked": true,"name": "item2 gai lan","labels": "","type": "ShoppingListItem","id": 3}, {"checked": false,"name": "item3 bananas","labels": "","type": "ShoppingListItem","id": 4}],"type": "ShoppingList","id": 1,"name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.body) # 'Expected list meta and items to be replaced.'
        expected_item1_name = expected_resource[ResourceKeys.ITEMS_KEY][0][ResourceKeys.NAME_KEY]
        self.assertTrue(response.body.find(expected_item1_name) >= 0)

    def test_update_shopping_list_meta(self):
        expected_resource = self.test_data.shopping_list_resource2
        # Update the already persisted list using the test's in memory (not yet persisted) resource dict
        newList1_id = get_id_str(self.test_data.newList1)
        expected_resource[ResourceKeys.ID_KEY] = newList1_id
        json_post_data = JsonHelper.serialize_to_json(expected_resource )
        rel_uri = '{0}/meta/'.format(newList1_id)
        response = self.http_client.put_rel_uri(rel_uri, httplib.OK, json_post_data)
        expected = '{"last_modified": "2011-03-09T19:48:21", "type": "ShoppingList", "id": 1, "name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.body)
        # Check getting updated meta.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        expected = '{"type": "ShoppingList","id": 1,"name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.body) # 'Expected list meta to be replaced, but items unchanged.'
        self.assertTrue(response.body.find('"{0}":'.format(ResourceKeys.ITEMS_KEY)) < 0)
        # Get the full list and ensure we didn't delete the items.
        rel_uri = '{0}/'.format(newList1_id)
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        expected = '{"items": [{"checked": false,"name": "item1 in list: Test List Name 1","labels": "","type": "ShoppingListItem","id": 1}],"type": "ShoppingList","id": 1,"name": "Test List Name 2 (From Resource)"}'
        self.assertEqualSanitizedJson(expected, response.body)

    def test_create_new_items(self):
        # Create in memory items
        item1_resource = self.test_data.create_item_resource('kei zi')
        item2_resource = self.test_data.create_item_resource('ngai gwa')
        item2_resource['checked'] = True
        item2_resource['id'] = -1
        action_resource = self.create_action_resource(ActionCrudConstants.CREATE,
            [ item1_resource, item2_resource ])

        json_post_data = JsonHelper.serialize_to_json(action_resource)
        newList1_id = get_id_str(self.test_data.newList1)
        # POST to create them.
        response = self.http_client.post_rel_uri(
            '{0}/items/'.format(newList1_id), httplib.CREATED, json_post_data)
        expected = '[{"checked": false, "name": "kei zi", "labels": "",  "type": "ShoppingListItem", "id": 2}, {"checked": true, "name": "ngai gwa", "labels": "",  "type": "ShoppingListItem", "id": 3}]'
        # Use _remove_last_modified to circumvent datetime.now() variance.
        self.assertEqualSanitizedJson(expected, response.body)

        # Assert in db
        actual_items_array = JsonHelper.deserialize_from_json(response.body)
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
        newItem1_id = get_id_str(self.test_data.newItem1)
        action_resource = self.create_action_resource( ActionCrudConstants.DELETE,
            [{ ResourceKeys.ID_KEY: newItem1_id }] )
        json_post_data = JsonHelper.serialize_to_json( action_resource )
        newList1_id = get_id_str(self.test_data.newList1)
        # DELETE
        response = self.http_client.post_rel_uri(
            '{0}/items/'.format(newList1_id), httplib.OK, json_post_data)
        self.assertEqual('', response.body)
        deleted_model1 = self.itemDao.get_by_id(self.test_data.newItem1.id)
        self.assertEqual(ModelStateConstants.DELETED, deleted_model1.state)

        # Get the list and check that our other items are there, but the deleted item is not.
        response = self.http_client.get_rel_uri('{0}/'.format(newList1_id), httplib.OK)
        resp_resource = JsonHelper.deserialize_from_json(response.body)
        found_item_ids = set([item_r[ResourceKeys.ID_KEY] for item_r in resp_resource[ResourceKeys.ITEMS_KEY]])
        self.assertTrue(not newItem1_id in found_item_ids)
        newItem2_id = get_id_str(newItem2)
        self.assertTrue(newItem2_id in found_item_ids)
        newItem3_id = get_id_str(newItem3)
        self.assertTrue(newItem3_id in found_item_ids)

        # Delete item2 and item3 in same request.
        action_resource = self.create_action_resource( ActionCrudConstants.DELETE,
            [{ ResourceKeys.ID_KEY: newItem2_id },
             { ResourceKeys.ID_KEY: newItem3_id }] )
        json_post_data = JsonHelper.serialize_to_json( action_resource )
        # DELETE
        response = self.http_client.post_rel_uri(
            '{0}/items/'.format(newList1_id), httplib.OK, json_post_data)
        self.assertEqual('', response.body)
        deleted_model2 = self.itemDao.get_by_id(newItem2_id)
        self.assertEqual(ModelStateConstants.DELETED, deleted_model2.state)
        deleted_model3 = self.itemDao.get_by_id(newItem3_id)
        self.assertEqual(ModelStateConstants.DELETED, deleted_model3.state)


class ShoppingListViewNoDataTest(ShoppingListTestBase):
    def setUp(self):
        super(ShoppingListViewNoDataTest, self).setUp()
        # Do not create any expected data (lists, items).

    def test_get_empty_shopping_list_index(self):
        # Ensure empty db
        self.mongo_helper.drop_database()
        self.assertEqual(0, self.listDao.get_count(), 'PRE: no shopping lists.')

        response = self.http_client.get_rel_uri('', httplib.OK)
        expected = '{"count": 0, "type": "ShoppingListIndex", "entries": []}'
        self.assertEqual(expected, response.body)
