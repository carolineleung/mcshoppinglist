import httplib
import sys
from mcshoppinglist.api.adapters.indexadapter import ShoppingListIndexAdapter
from mcshoppinglist.api.adapters.listadapter import ShoppingListAdapter
from mcshoppinglist.api.views.helpers import ViewRequestHelper, ViewResponseHelper
from mcshoppinglist.shared.exceptions import ShoppingListError
from mcshoppinglist.shared.helpers import  JsonHelper
from mcshoppinglist.shared.logfactory import LogFactory

logger = LogFactory.get_logger(__name__)

class ShoppingListIndexView(object):
    def __init__(self):
        self.req_helper = ViewRequestHelper()
        self.resp_helper = ViewResponseHelper()

    def _shopping_list_index_get(self):
        """
        Return a list of (JSON) ShoppingList (without the items)
        """
        # TODO Does Django return a 500 status code on unhnadled exceptions, or do we need to try/catch here?
        resource = None
        try:
            adapter = ShoppingListIndexAdapter()
            resource = adapter.adapt_to_resource()
        except Exception:
            logger.exception('Failed to create shopping list index resource.')
            raise
        try:
            json_data = JsonHelper.serialize_to_json(resource)
            return self.resp_helper.create_json_http_response(json_data)
        except Exception:
            logger.exception('Failed to serialize shopping list index to JSON.')
            raise

    def _create_new_shopping_list(self, request):
        """
        Create a new ShoppingList from the POST method body (JSON).
        returns: Response with the new ShoppingList (JSON) without the items
        """
        list_model = None
        try:
            adapter = ShoppingListAdapter()
            # request.POST is expected to be a dictionary. If clients pass a JSON encoded object, it's not a dict.
            resource_from_json = self.req_helper.deserialize_post_data_from_json(request)
            list_model = adapter.create_from_resource(resource_from_json)
        except Exception:
            raise ShoppingListError('Failed to create new shopping list. {0} '.format(sys.exc_info()))
        if not list_model or not hasattr(list_model, 'id'):
            raise ShoppingListError('Failed to serialize shopping list index to JSON. (No model created.)')

        logger.info('Created new ShoppingList id:{0}'.format(list_model.id))

        try:
            adapter = ShoppingListAdapter()
            # Don't include all items, just the shopping list meta data
            resource = adapter.adapt_to_resource(list_model, include_items=False)
            response = self.resp_helper.create_serialized_json_response(resource, list_model)
            response.status_int = httplib.CREATED
            return response
        except Exception as ex:
            msg = 'Failed to serialize newly created shopping list {0} to JSON.'.format(list_model.id)
            logger.exception(msg)
            raise ShoppingListError(msg, ex)

    def shopping_list_index_handler(self, request):
        if request.method == 'GET':
            return self._shopping_list_index_get()
        elif request.method == 'POST':
            return self._create_new_shopping_list(request)
        # 405 per http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        return self.resp_helper.create_response_not_allowed(['GET', 'POST'])