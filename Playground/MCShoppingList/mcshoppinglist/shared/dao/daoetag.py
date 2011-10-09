from datetime import datetime
from mcshoppinglist.etags.etagmanager import EtagManager
from mcshoppinglist.shared.dao.daobase import DaoBase, fix_state
from mcshoppinglist.shared.exceptions import ShoppingListError

class DaoWithEtagBase(DaoBase):
    def save_etag(self, etag_manager, model):
        """
        Save the etag for the model using the etag_manager.
        Intended to be overridden by derived classes.
        """
        etag_manager.save_etag(model)

    def save(self, model):
        fix_state(model) # TODO Revisit this ugly way of guaranteeing state
        super(DaoWithEtagBase, self).save(model)
        try:
            etag_manager = EtagManager()
            self.save_etag(etag_manager, model)
        except Exception as ex:
            id_str = ''
            try:
                id_str = model.id
            except:
                pass
            raise ShoppingListError('Failed to save etag. ShoppingListItem id: {0}'.format(id_str), ex)