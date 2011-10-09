import httplib
from mcshoppinglist.api.adapters.itemadapter import ShoppingListItemAdapter
from mcshoppinglist.api.adapters.listadapter import ShoppingListAdapter
from mcshoppinglist.api.constants import ResourceKeys, ActionCrudConstants
from mcshoppinglist.api.helpers import ShoppingListItemUpdateResponseFactory
from mcshoppinglist.api.views.helpers import ViewRequestHelper, ViewResponseHelper
from mcshoppinglist.shared.exceptions import ShoppingListError, HttpResponseError
from mcshoppinglist.shared.helpers import   InspectHelper
from mcshoppinglist.shared.logfactory import LogFactory
from mcshoppinglist.shoppinglists.dao import  ShoppingListItemDao

logger = LogFactory.get_logger(__name__)

class ShoppingListItemView(object):
    def __init__(self):
        self.req_helper = ViewRequestHelper()
        self.resp_helper = ViewResponseHelper()

    def _update_list_items(self, list_model, item_resources):
        """
        Update items in the ShoppingList using the request body item resource array:  [ {item1} ].
        item_resources: [ {item1}, {item2}...]  as ShoppingListItem resource dictionaries.
        returns: Response with list of updated (JSON) ShoppingListItem [ {item1}, {item2} ... ]
        """
        # Update each item per the request.
        updated_resource_list = []
        try:
            adapter = ShoppingListItemAdapter()
            # TODO This handling should be best effort rather than first-failure-aborts, and should return a status (JSON) in the response body indicating which updates succeeded and which failed.
            for item_resource in item_resources:
                if not InspectHelper.isdict(item_resource):
                    raise ShoppingListError('Invalid ShoppingListItem resource: {0}'.format(item_resource))
                updated_item_model = adapter.update_from_resource(item_resource)
                logger.info('Updated ShoppingListItem id: {0}'.format(updated_item_model.id))
                updated_resource = adapter.adapt_to_resource(updated_item_model)
                updated_resource_list.append(updated_resource)
        except Exception:
            logger.exception('Failed to update model from resource.')
            raise

        # Serialize the list of updated item resources and include in response.
        try:
            response_factory = ShoppingListItemUpdateResponseFactory()
            response_resource = response_factory.create_response_from_resource_list(updated_resource_list)
            response = self.resp_helper.create_serialized_json_response(response_resource, list_model)
            return response
        except Exception:
            logger.exception('Model was successfully updated from resources. Failed to serialize JSON response.')
            raise


    def _create_new_list_items(self, list_model, item_resources):
        """
        Create new ShoppingListItem from the request's item array.
        item_resources: [ {item1}, {item2}...]  as ShoppingListItem resource dictionaries.
        """
        item_adapter = ShoppingListItemAdapter()
        items_list = []
        for new_item in item_resources:
            item_model = item_adapter.create_from_resource(new_item, list_model)
            # Return the new items so the client knows their newly assigned IDs
            items_list.append(item_model)
            logger.info('Created new item {0} in ShoppingList {1}'.format(item_model.id, list_model.id))
        list_adapter = ShoppingListAdapter()
        items_list_resource = list_adapter.adapt_items_list_to_resource(items_list)
        response = self.resp_helper.create_serialized_json_response(items_list_resource, list_model)
        response.status_int = httplib.CREATED
        # TODO Location header for all POSTs: If a resource has been created on the origin server, the response SHOULD be 201 (Created) and contain an entity which describes the status of the request and refers to the new resource, and a Location header (see section 14.30). http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.7
        return response

    def _delete_list_items(self, list_model, item_resources):
        if not item_resources or not InspectHelper.isiterable(item_resources):
            return
        dao = ShoppingListItemDao()
        for existing_item in item_resources:
            if InspectHelper.isdict(existing_item) and ResourceKeys.ID_KEY in existing_item:
                item_model = dao.get_by_id(existing_item[ResourceKeys.ID_KEY], list_model)
                if item_model:
                    dao.mark_item_deleted(item_model)
                    logger.info('Marked ShoppingListItem {0} as deleted.'.format(item_model.id))
        # OK
        return self.resp_helper.create_empty_ok_response()

    def _shopping_list_items_post(self, request, list_id):
        """
        request body:   {  action: a, items: [ {item1}, {item2} ... ] }
        """
        list_model = self.req_helper.get_shopping_list_model(list_id)
        action_resource = self.req_helper.deserialize_post_data_from_json(request)

        error_msg = None
        if(not action_resource or not InspectHelper.isdict(action_resource)
           or not ResourceKeys.ACTION_KEY in action_resource):
            error_msg = 'Invalid request. Missing property: {0}'.format(ResourceKeys.ACTION_KEY)
        elif not ResourceKeys.ITEMS_KEY in action_resource:
            error_msg = 'Invalid request. Missing property: {0}'.format(ResourceKeys.ITEMS_KEY)
        elif not InspectHelper.isiterable(action_resource[ResourceKeys.ITEMS_KEY]):
            error_msg = 'Invalid request. Property: {0} must be an array.'.format(ResourceKeys.ITEMS_KEY)

        if error_msg:
            raise HttpResponseError(error_msg, status_int=httplib.BAD_REQUEST)

        action = action_resource[ResourceKeys.ACTION_KEY]
        if action == ActionCrudConstants.CREATE:
            return self._create_new_list_items(list_model, action_resource[ResourceKeys.ITEMS_KEY])
        elif action == ActionCrudConstants.UPDATE:
            return self._update_list_items(list_model, action_resource[ResourceKeys.ITEMS_KEY])
        elif action == ActionCrudConstants.DELETE:
            return self._delete_list_items(list_model, action_resource[ResourceKeys.ITEMS_KEY])
        else:
            raise HttpResponseError('Invalid {0}: {1}'.format(
                ResourceKeys.ACTION_KEY, action), status_int=httplib.BAD_REQUEST)

    def shopping_list_items_handler(self, request):
        list_id = self.req_helper.get_list_id(request)
        # TODO The action performed by the POST method might not result in a resource that can be identified by a URI. In this case, either 200 (OK) or 204 (No Content) is the appropriate response status, depending on whether or not the response includes an entity that describes the result. http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.7
        if request.method == 'POST':
            return self._shopping_list_items_post(request, list_id)
        # 405 per http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        return self.resp_helper.create_response_not_allowed(['POST'])