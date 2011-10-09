import httplib
from mcshoppinglist.api.constants import ResourceKeys
from mcshoppinglist.shared.helpers import JsonHelper
from mcshoppinglist.shared.models.constants import ModelStateConstants
from mcshoppinglist.shared.models.helpers import get_id_str
from mcshoppinglist.test.shared.base import ShoppingListTestBase
from mcshoppinglist.test.shared.httphelpers import EtagResponseDataSnapshot
from mcshoppinglist.test.shared.shoppinglisttestdata import ShoppingListTestDataOneItem


# TODO Add test for if we just change the shopping list model, not the item
# TODO Add tests for multiple items changing
class ShoppingListViewDiffTest(ShoppingListTestBase):
    def setUp(self):
        super(ShoppingListViewDiffTest, self).setUp()
        self.test_data = ShoppingListTestDataOneItem()

    def test_get_shopping_list_diff_full_no_etag(self):
        self.http_client.get_rel_uri(
            '{0}/diff/'.format(self.test_data.newList1.id), httplib.OK)
        # TODO assert response.body

    def test_get_shopping_list_diff_invalid_etag(self):
        self.http_client.get_rel_uri(
            '{0}/diff/'.format(self.test_data.newList1.id), httplib.OK, etag_header='INVALID_ETAG')
        # TODO assert response.body

    def test_get_shopping_list_diff(self):
        rel_uri = '{0}/diff/'.format(self.test_data.newList1.id)
        # With no conditional GET (no If-Modified-Since/If-None-Match), expect the full list and an etag.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        response_snap1 = EtagResponseDataSnapshot(response, self)
        # TODO assert response.body

        # Check for 304 not modified
        response = self.http_client.get_rel_uri(rel_uri, httplib.NOT_MODIFIED, etag_header=response_snap1.etag)
        self.assertEqual('', response.body)

        # Check for same shopping list items when we include an invalid ETag.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header='INVALID_ETAG')
        self.assertEqual(response_snap1.response.body, response.body)

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
        self.assertTrue(response.body.find(self.test_data.newItem1.name) >= 0)

        # Check for 304 not modified, with the new etag
        response = self.http_client.get_rel_uri(rel_uri, httplib.NOT_MODIFIED, etag_header=response_snap2.etag)
        self.assertEqual('', response.body)

        # Add a new item
        newItem2 = self.test_data.create_and_save_new_item(self.test_data.newList1, 'granola')

        # Check that we get only the new item using the old etag
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header=response_snap2.etag)
        response_snap3 = EtagResponseDataSnapshot(response, self)
        # TODO Better asserts for content
        self.assertTrue(response.body.find(self.test_data.newItem1.name) < 0)
        self.assertTrue(response.body.find(newItem2.name) >= 0)

        # Check that we get a 304 now for the new item
        response = self.http_client.get_rel_uri(rel_uri, httplib.NOT_MODIFIED, etag_header=response_snap3.etag)
        self.assertEqual(0, len(response.body))

        # Update both items
        self.test_data.newItem1.name += ' again'
        self.itemDao.save(self.test_data.newItem1)
        newItem2.name += ' updated'
        self.itemDao.save(newItem2)

        # Ensure both updated items are returned
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header=response_snap3.etag)
        #response_snap4 = ResponseDataSnapshot(response, self)
        # TODO Better asserts re. content
        self.assertTrue(response.body.find(self.test_data.newItem1.name) >= 0)
        self.assertTrue(response.body.find(newItem2.name) >= 0)

    def test_get_shopping_list_diff_deleted(self):
        # Create a second and third item so the first item isn't lonely.
        newItem2 = self.test_data.create_and_save_new_item(self.test_data.newList1, 'item2')
        newItem3 = self.test_data.create_and_save_new_item(self.test_data.newList1, 'item3')

        rel_uri = '{0}/diff/'.format(self.test_data.newList1.id)
        # With no conditional GET (no If-Modified-Since/If-None-Match), expect the full list and an etag.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        # TODO assert response.body
        response_snap1 = EtagResponseDataSnapshot(response, self)

        # Delete the first item
        self.itemDao.delete(self.test_data.newItem1)

        # Get the diff, expect item marked deleted
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK, etag_header=response_snap1.etag)
        #response_snap2 = ResponseDataSnapshot(response, self)
        response_resource2 = JsonHelper.deserialize_from_json(response.body)
        items_resource2 = response_resource2['items']
        self.assertEqual(1, len(items_resource2), msg='Expected diff to show deleted item.')
        self.assertEqual(get_id_str(self.test_data.newItem1), items_resource2[0][ResourceKeys.ID_KEY])
        self.assertEqual(ModelStateConstants.DELETED, items_resource2[0][ResourceKeys.STATE_KEY])

        # Get the full list (no etag), expect the deleted item to be present.
        response = self.http_client.get_rel_uri(rel_uri, httplib.OK)
        self.assertTrue(response.body.find('"id": "{0}"'.format(get_id_str(self.test_data.newItem1))) >= 0)
        # TODO assert id 1 state == DELETED
        self.assertTrue(response.body.find('"id": "{0}"'.format(get_id_str(newItem2))) >= 0)
        self.assertTrue(response.body.find('"id": "{0}"'.format(get_id_str(newItem3))) >= 0)

        # TODO Additional tests: delete more items, check again.





