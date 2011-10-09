from mcshoppinglist.api.adapters.listadapter import  ShoppingListAdapter
from mcshoppinglist.api.views.helpers import ViewRequestHelper, ViewResponseHelper
from mcshoppinglist.shared.exceptions import ShoppingListError
from mcshoppinglist.shared.logfactory import LogFactory

logger = LogFactory.get_logger(__name__)

class ShoppingListView(object):
    def __init__(self):
        self.req_helper = ViewRequestHelper()
        self.resp_helper = ViewResponseHelper()

    def get_shopping_list_detail(self, list_id, since_last_modified=None,
                              include_deleted_items=False, include_etag_headers=False, include_items=True):
        """
        returns: Response with JSON representation of the ShoppingList and all its ShoppingListItems
        """

        # TODO Return 304 if ETag matches latest
        list_model = self.req_helper.get_shopping_list_model(list_id)
        try:
            adapter = ShoppingListAdapter()
            list_resource = adapter.adapt_to_resource(list_model,
                include_items=include_items, since_last_modified=since_last_modified,
                include_deleted_items=include_deleted_items)
            response = self.resp_helper.create_serialized_json_response(
                list_resource, list_model, include_etag_headers=include_etag_headers)
            return response
        except Exception as ex:
            msg = 'Failed to get shopping list resource with id {0}'.format(list_id)
            logger.exception(msg)
            # 500
            raise ShoppingListError(msg, ex)

    def _update_shopping_list_detail(self, request, list_id, include_items=True):
        """
        Replace all items and metadata for the ShoppingList with the request's data.
        """
        # TODO Exception handling
        adapter = ShoppingListAdapter()
        updated_list_resource = self.req_helper.deserialize_post_data_from_json(request)
        list_model = adapter.update_from_resource(list_id, updated_list_resource, include_items=include_items)
        logger.info('Updated (replaced) shopping list and its items. ShoppingList id: {0}'.format(list_model.id))
        list_resource = adapter.adapt_to_resource(list_model, include_items=include_items)
        response = self.resp_helper.create_serialized_json_response(list_resource, list_model)
        return response


    def shopping_list_detail_handler(self, request):
        list_id = self.req_helper.get_list_id(request)
        # TODO response headers, mime type etc.: http://blog.nullobject.ca/2010/02/08/django-json-woes/
        if request.method == 'GET':
            return self.get_shopping_list_detail(list_id, include_etag_headers=True)
        elif request.method == 'PUT':
            return self._update_shopping_list_detail(request, list_id)
        # 405 per http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        return self.resp_helper.create_response_not_allowed(['GET', 'PUT'])

    def shopping_list_meta_handler(self, request):
        list_id = self.req_helper.get_list_id(request)
        if request.method == 'GET':
            return self.get_shopping_list_detail( list_id, include_items=False)
        elif request.method == 'PUT':
            return self._update_shopping_list_detail(request, list_id, include_items=False)
        return self.resp_helper.create_response_not_allowed(['GET', 'PUT'])

