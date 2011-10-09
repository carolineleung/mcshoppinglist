import httplib
import logging
import re
import sys
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotModified
from dependencyresolver import DependencyResolver
from shoppinglists.api import   ShoppingListAdapter, ShoppingListIndexAdapter, ShoppingListItemAdapter, ShoppingListItemUpdateResponseFactory, ResourceKeys, ActionCrudConstants
from shoppinglists.exceptions import ShoppingListError, HttpResponseError
from shoppinglists.handlerwrapper import RequestHandlerWrapper
from shoppinglists.helpers import JsonHelper, InspectHelper
from shoppinglists.models import  EtagCacheEntry, ShoppingListDao, ShoppingListItemDao

logger = logging.getLogger(__name__)

# TODO In all responses, tweak response headers, mime type etc.: http://blog.nullobject.ca/2010/02/08/django-json-woes/
# TODO Add Location headers where appropriate for new resources. (Updated too? Check http spec.)
# TODO Idempotent DELETE, particularly of entire shopping lists!   The DELETE method is idempotent. This implies that the server must return response code 200 (OK) even if the server deleted the resource in a previous request. But in practice, implementing DELETE as an idempotent operation requires the server to keep track of all deleted resources. Otherwise, it can return a 404 (Not Found).

def _create_json_http_response(json_content, status_code=httplib.OK):
    return HttpResponse(json_content, status=status_code, content_type=JsonHelper.JSON_CONTENT_TYPE)

def _deserialize_post_data_from_json(request):
    try:
        resource = JsonHelper.deserialize_from_json(request.raw_post_data)
        return resource
    except Exception as ex:
        request_data_str = ''
        if hasattr(request, 'raw_post_data') and request.raw_post_data:
            request_data_str = request.raw_post_data
        msg = 'Failed to parse request content. POST data:\n{0}'.format(request_data_str)
        logger.exception(msg)
        raise ShoppingListError(msg, ex)

def _shopping_list_index_get(request):
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
        return _create_json_http_response(json_data)
    except Exception:
        logger.exception('Failed to serialize shopping list index to JSON.')
        raise

def _create_new_shopping_list(request):
    """
    Create a new ShoppingList from the POST method body (JSON).
    returns: HttpResponse with the new ShoppingList (JSON) without the items
    """
    list_model = None
    try:
        adapter = ShoppingListAdapter()
        # request.POST is expected to be a dictionary. If clients pass a JSON encoded object, it's not a dict.
        resource_from_json = JsonHelper.deserialize_from_json(request.raw_post_data)
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
        response = _create_serialized_json_response(resource, list_model)
        response.status_code = httplib.CREATED
        return response
    except Exception as ex:
        msg = 'Failed to serialize newly created shopping list {0} to JSON.'.format(list_model.id)
        logger.exception(msg)
        raise ShoppingListError(msg, ex)

def _shopping_list_index_handler(request):
    if request.method == 'GET':
        return _shopping_list_index_get(request)
    elif request.method == 'POST':
        return _create_new_shopping_list(request)
    # 405 per http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    return HttpResponseNotAllowed(('GET', 'POST'))

def shopping_list_index(request):
    return RequestHandlerWrapper.handle(_shopping_list_index_handler, request)

#    shoppingLists = ShoppingList.objects.all()[:10] #.order_by('-pub_date')[:5]
#    return render_to_response('shoppinglists/index.html', {'shoppingLists': shoppingLists})

#class MyJsonSerializer(json.Serializer):
#    # From:  django\core\serializers\python.py
#    def end_object(self, obj):
##        self.objects.append({
##            "model"  : smart_unicode(obj._meta),
##            "pk"     : smart_unicode(obj._get_pk_val(), strings_only=True),
##            "fields" : self._current
##        })
##        self._current = None
#        self._current["id"] = smart_unicode(obj._get_pk_val(), strings_only=True)
#        self.objects.append(self._current)
#        self._current = None

def _get_shopping_list_model(list_id):
    """
    returns: ShoppingList model
    exception: if ShoppingList not found
    """
    list_model = None
    try:
        dao = ShoppingListDao()
        list_model = dao.get_by_id(list_id)
    except Exception:
        logger.exception('Failed to get shopping list id {0}'.format(list_id))
    if not list_model:
        # 404
        raise HttpResponseError(
            'Resource not found. Failed to find shopping list with id: {0}'.format(list_id),
            status_code=httplib.NOT_FOUND
        )
    return list_model

def _set_response_headers(response, model_for_etag):
    # TODO response headers, mime type etc.: http://blog.nullobject.ca/2010/02/08/django-json-woes/
    # TODO Fix headers....  Other cache headers
    etag_model = DependencyResolver.get_etag_manager().get_etag_model(model_for_etag)
    response['ETag'] = '"{0}"'.format(etag_model.etag)
    # Use etag last modified (so it includes last_modified of items)
    response['Last-Modified'] = '{0}'.format(etag_model.last_modified)

def _create_serialized_json_response(resource_data, shopping_list_model, include_etag_headers=False):
    """
    resource_data: dict or array representing the resource to serialize.
    """
    json_data = JsonHelper.serialize_to_json(resource_data)
    # 200 OK
    response = _create_json_http_response(json_data)
    if include_etag_headers:
        _set_response_headers(response, shopping_list_model)
    return response

def _get_shopping_list_detail(request, list_id, since_last_modified=None,
                              include_deleted_items=False, include_etag_headers=False, include_items=True):
    """
    returns: HttpResponse with JSON representation of the ShoppingList and all its ShoppingListItems
    """
    list_model = _get_shopping_list_model(list_id)

    try:
        adapter = ShoppingListAdapter()
        list_resource = adapter.adapt_to_resource(list_model,
            include_items=include_items, since_last_modified=since_last_modified,
            include_deleted_items=include_deleted_items)
        response = _create_serialized_json_response(list_resource, list_model,
                                                    include_etag_headers=include_etag_headers)
        return response
    except Exception as ex:
        msg = 'Failed to get shopping list resource with id {0}'.format(list_id)
        logger.exception(msg)
        # 500
        raise ShoppingListError(msg, ex)

def _update_shopping_list_detail(request, list_id, include_items=True):
    """
    Replace all items and metadata for the ShoppingList with the request's data.
    """
    # TODO Exception handling
    adapter = ShoppingListAdapter()
    updated_list_resource = _deserialize_post_data_from_json(request)
    list_model = adapter.update_from_resource(list_id, updated_list_resource, include_items=include_items)
    logger.info('Updated (replaced) shopping list and its items. ShoppingList id: {0}'.format(list_model.id))
    list_resource = adapter.adapt_to_resource(list_model, include_items=include_items)
    response = _create_serialized_json_response(list_resource, list_model)
    return response

def _shopping_list_detail_handler(request, list_id):
    # TODO response headers, mime type etc.: http://blog.nullobject.ca/2010/02/08/django-json-woes/
    if request.method == 'GET':
        return _get_shopping_list_detail(request, list_id, include_etag_headers=True)
    elif request.method == 'PUT':
        return _update_shopping_list_detail(request, list_id)
    # 405 per http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    return HttpResponseNotAllowed(('GET', 'PUT'))

def shopping_list_detail(request, list_id):
    return RequestHandlerWrapper.handle(_shopping_list_detail_handler, request, list_id)

def _shopping_list_meta_handler(request, list_id):
    if request.method == 'GET':
        return _get_shopping_list_detail(request, list_id, include_items=False)
    elif request.method == 'PUT':
        return _update_shopping_list_detail(request, list_id, include_items=False)
    return HttpResponseNotAllowed(('GET', 'PUT'))

def shopping_list_meta(request, list_id):
    return RequestHandlerWrapper.handle(_shopping_list_meta_handler, request, list_id)

def _update_list_items(list_model, item_resources):
    """
    Update items in the ShoppingList using the request body item resource array:  [ {item1} ].
    item_resources: [ {item1}, {item2}...]  as ShoppingListItem resource dictionaries.
    returns: HttpResponse with list of updated (JSON) ShoppingListItem [ {item1}, {item2} ... ]
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
        response = _create_serialized_json_response(response_resource, list_model)
        return response
    except Exception:
        logger.exception('Model was successfully updated from resources. Failed to serialize JSON response.')
        raise


def _create_new_list_items(list_model, item_resources):
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
    response = _create_serialized_json_response(items_list_resource, list_model)
    response.status_code = httplib.CREATED
    # TODO Location header for all POSTs: If a resource has been created on the origin server, the response SHOULD be 201 (Created) and contain an entity which describes the status of the request and refers to the new resource, and a Location header (see section 14.30). http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.7
    return response

def _delete_list_items(list_model, item_resources):
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
    return HttpResponse()

def _shopping_list_items_post(request, list_id):
    """
    request body:   {  action: a, items: [ {item1}, {item2} ... ] }
    """
    list_model = _get_shopping_list_model(list_id)
    action_resource = _deserialize_post_data_from_json(request)

    error_msg = None
    if(not action_resource or not InspectHelper.isdict(action_resource)
       or not ResourceKeys.ACTION_KEY in action_resource):
        error_msg = 'Invalid request. Missing property: {0}'.format(ResourceKeys.ACTION_KEY)
    elif not ResourceKeys.ITEMS_KEY in action_resource:
        error_msg = 'Invalid request. Missing property: {0}'.format(ResourceKeys.ITEMS_KEY)
    elif not InspectHelper.isiterable(action_resource[ResourceKeys.ITEMS_KEY]):
        error_msg = 'Invalid request. Property: {0} must be an array.'.format(ResourceKeys.ITEMS_KEY)

    if error_msg:
        raise HttpResponseError(error_msg, status_code=httplib.BAD_REQUEST)

    action = action_resource[ResourceKeys.ACTION_KEY]
    if action == ActionCrudConstants.CREATE:
        return _create_new_list_items(list_model, action_resource[ResourceKeys.ITEMS_KEY])
    elif action == ActionCrudConstants.UPDATE:
        return _update_list_items(list_model, action_resource[ResourceKeys.ITEMS_KEY])
    elif action == ActionCrudConstants.DELETE:
        return _delete_list_items(list_model, action_resource[ResourceKeys.ITEMS_KEY])
    else:
        raise HttpResponseError('Invalid {0}: {1}'.format(
            ResourceKeys.ACTION_KEY, action), status_code=httplib.BAD_REQUEST)

def _shopping_list_items_handler(request, list_id):
    # TODO The action performed by the POST method might not result in a resource that can be identified by a URI. In this case, either 200 (OK) or 204 (No Content) is the appropriate response status, depending on whether or not the response includes an entity that describes the result. http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.7
    if request.method == 'POST':
        return _shopping_list_items_post(request, list_id)
    # 405 per http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    return HttpResponseNotAllowed(('POST'))

def shopping_list_items(request, list_id):
    return RequestHandlerWrapper.handle(_shopping_list_items_handler, request, list_id)

def _get_etag_from_request(request):
    etag = None
    try:
        if_none_match_key = 'HTTP_IF_NONE_MATCH' # Django converts If-None-Match to uppercase with _
        if if_none_match_key in request.META:
            # TODO Can we make key lookup case insensitive?
            request_etags = request.META[if_none_match_key]
            if request_etags:
                # http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
                # If-None-Match: "xyzzy", "r2d2xxxx", "c3piozzzz"

                # Take the first etag in list. Client should not be sending multiple.
                split_etags = request_etags.split(',')
                if split_etags and len(split_etags) > 0 and split_etags[0] and len(split_etags[0]) > 0:
                    # split_etags[0] = '"xyzzy" '
                    # Remove the quotes and whitespace
                    etag = re.sub(r'^\s*"+', '', split_etags[0])
                    etag = re.sub(r'"+\s*$', '', etag)
                    # etag = 'xyzzy'
    except Exception as ex:
        logger.warn('Failed to parse ETag from request. Cause: {0}'.format(ex.message), ex)
    return etag

def _shopping_list_diff_get(request, list_id):
    since_last_modified = None
    # ETag parsing errors should not be fatal to the request.
    try:
        request_etag = _get_etag_from_request(request)
        if request_etag and len(request_etag) > 0:
            logger.debug('Got ETag from request: {0}'.format(request_etag))
            etag_queryset = EtagCacheEntry.objects.filter(etag__exact=request_etag)
            if etag_queryset and etag_queryset.count() > 0:
                logger.debug('ETag matched. Not modified. {0}'.format(request_etag))
                response = HttpResponseNotModified()
                # Include the matched etag per http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
                response['ETag'] = request_etag
                # TODO Include other cache headers
                return response
            else:
                logger.debug('ETag not matched. Extracting last_modified. {0}'.format(request_etag))
                try:
                    since_last_modified = DependencyResolver.get_etag_manager().get_last_modified_from_etag(request_etag)
                    logger.debug('ETag not matched. {0}  since_last_modified: {1}'.format(request_etag, since_last_modified))
                except Exception as ex2:
                    logger.warn('Failed to parse request header ETag: {0}  Cause: {1}'.format(
                        request_etag, ex2.message), exc_info=1)
        # else:
        # TODO else Handle If-Modified-Since. Per http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        # "If none of the entity tags match, then the server MAY perform the requested method as if the If-None-Match header field did not exist, but MUST also ignore any If-Modified-Since header field(s) in the request. That is, if no entity tags match, then the server MUST NOT return a 304 (Not Modified) response."
    except Exception as ex:
        logger.error('Failed to process request header ETag. Cause: {0}'.format(ex.message), exc_info=1)
    return _get_shopping_list_detail(request, list_id, since_last_modified=since_last_modified,
                                     include_deleted_items=True, include_etag_headers=True)

def _shopping_list_diff_handler(request, list_id):
    if request.method == 'GET':
        return _shopping_list_diff_get(request, list_id)
    # 405 per http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    return HttpResponseNotAllowed(('GET'))

def shopping_list_diff(request, list_id):
    return RequestHandlerWrapper.handle(_shopping_list_diff_handler, request, list_id)

