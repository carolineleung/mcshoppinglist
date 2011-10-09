from mcshoppinglist.etags.dao import EtagCacheEntryDao

from mcshoppinglist.etags.etagmanager import EtagManager
from mcshoppinglist.shoppinglists.models import  ShoppingList, ShoppingListItem
from mcshoppinglist.test.shared.base import ShoppingListTestBase

class DaoTest(ShoppingListTestBase):
    def setUp(self):
        super(DaoTest, self).setUp()

    def _create_list_model(self, list_name='name = test list'):
        list_model = ShoppingList()
        list_model.name = list_name
        self.listDao.save(list_model)

        refreshed_list_model = self.listDao.get_by_id(list_model.id)
        self.assertEqual(list_model.id, refreshed_list_model.id)
        self.assertEqual(list_model.name, refreshed_list_model.name)
        return list_model

    def test_list_dao(self):
        self._create_list_model(list_name='name = test_list_dao list')

    def _check_item_model(self, expected_item_model):
        refreshed_item_model = self.itemDao.get_by_id(expected_item_model.id)
        self.assertEqual(expected_item_model.id, refreshed_item_model.id)
        self.assertEqual(expected_item_model.name, refreshed_item_model.name)
        self.assertEqual(expected_item_model.checked, refreshed_item_model.checked)

    def _create_item_model(self, list_model, item_name='name = test item'):
        item_model = ShoppingListItem()
        item_model.name = item_name
        item_model.checked = True
        item_model.shopping_list = list_model

        self.itemDao.save(item_model)
        self._check_item_model(item_model)
        return item_model

    def test_item_dao(self):
        list_model = self._create_list_model(list_name='name = test_item_dao list')
        item_model = self._create_item_model(list_model, item_name='name = test_item_dao item')

        # Update the item
        item_id = item_model.id
        item_model.name += ' updated'
        self.itemDao.save(item_model)
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