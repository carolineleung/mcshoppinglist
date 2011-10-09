from mcshoppinglist.api.adapters.indexadapter import ShoppingListIndexAdapter
from mcshoppinglist.api.adapters.itemadapter import ShoppingListItemAdapter
from mcshoppinglist.api.adapters.listadapter import ShoppingListAdapter
from mcshoppinglist.api.constants import ResourceKeys
from mcshoppinglist.test.shared.base import ShoppingListTestBase
from mcshoppinglist.test.shared.shoppinglisttestdata import ShoppingListTestDataOneItem

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