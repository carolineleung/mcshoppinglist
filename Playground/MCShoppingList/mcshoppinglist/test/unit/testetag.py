from mcshoppinglist.etags.etagmanager import EtagManager
from mcshoppinglist.test.shared.base import ShoppingListTestBase
from mcshoppinglist.test.shared.shoppinglisttestdata import ShoppingListTestDataOneItem


class EtagManagerTest(ShoppingListTestBase):
    def setUp(self):
        super(EtagManagerTest, self).setUp()
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