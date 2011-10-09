from mcshoppinglist.shared.dao.daoetag import DaoWithEtagBase
from mcshoppinglist.shared.models.constants import ModelStateConstants
from mcshoppinglist.shoppinglists.models import  ShoppingList, ShoppingListItem

class ShoppingListDao(DaoWithEtagBase):
    def get_count(self):
        # TODO Does this RETRIEVE all documents??? More efficient way to get a count?
        return self.get_all().count()

    def get_all(self):
        return ShoppingList.objects.filter(state__ne=ModelStateConstants.DELETED)

    def get_by_id(self, id):
        return self.get_by_id_from_objects(id, ShoppingList.objects)

class ShoppingListItemDao(DaoWithEtagBase):
    def save_etag(self, etag_manager, model):
        # Use the ShoppingList for ETag id, but our ShoppingListItem last_modified.
        # This routes both ShoppingList and ShoppingListItem to the same ETag.
        etag_manager.save_etag(model.shopping_list, model.last_modified)

    def get_by_id(self, id, shopping_list_model=None):
        """
        shopping_list_model: when not None, restrict the get to only
        """
        if shopping_list_model:
            qs = ShoppingListItem.objects.filter(id=id, shopping_list=shopping_list_model)
            # TODO Assert? Should never be more than one matching exact id!
            if qs and qs.count() > 0 and qs[0]:
                return qs[0]
            return None
        else:
            return self.get_by_id_from_objects(id, ShoppingListItem.objects)

    def get_by_shopping_list_model(self, shopping_list_model, since_last_modified=None, include_deleted_items=False):
        filter_kwargs = { 'shopping_list': shopping_list_model }

        if since_last_modified:
            filter_kwargs['last_modified__gt'] = since_last_modified
        if not include_deleted_items:
            filter_kwargs['state__ne'] = ModelStateConstants.DELETED

        return ShoppingListItem.objects.filter(**filter_kwargs)

    def mark_item_deleted(self, item_model):
        item_model.state = ModelStateConstants.DELETED
        item_model.save()

    def mark_items_deleted(self, shopping_list_model):
        """
        shopping_list_model: a ShoppingList model
        """
        delete_items_queryset = ShoppingListItem.objects.filter(shopping_list=shopping_list_model)
        if delete_items_queryset and delete_items_queryset.count() > 0:
            # delete_items_queryset.delete()
            for item_to_delete in delete_items_queryset:
                self.mark_item_deleted(item_to_delete)

