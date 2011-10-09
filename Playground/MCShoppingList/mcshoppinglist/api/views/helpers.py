from datetime import datetime
import httplib
import logging
from webob.response import Response
from mcshoppinglist.api.views.constants import  RequestKeys
from mcshoppinglist.etags.etagmanager import EtagManager
from mcshoppinglist.shared.exceptions import ShoppingListError, HttpResponseError
from mcshoppinglist.shared.helpers import HttpResponseHelper, JsonHelper
from mcshoppinglist.shoppinglists.dao import ShoppingListDao

logger = logging.getLogger(__name__)

class ViewRequestHelper(object):
    def get_list_id(self, request):
        if not RequestKeys.LIST_ID_KEY in request.matchdict:
            raise HttpResponseError('Missing URL component: {0}'.format(RequestKeys.LIST_ID_KEY),
                                    status_int=httplib.BAD_REQUEST)
        return request.matchdict[RequestKeys.LIST_ID_KEY]

    def get_shopping_list_model(self, list_id):
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
                status_int=httplib.NOT_FOUND
            )
        return list_model

    def deserialize_post_data_from_json(self, request):
        try:
            resource = JsonHelper.deserialize_from_json(request.body)
            return resource
        except Exception as ex:
            request_data_str = ''
            try:
                if hasattr(request, 'body') and request.body:
                    request_data_str = request.body
            except:
                pass # Ignore
            msg = 'Failed to parse request content. POST data:\n{0}'.format(request_data_str)
            logger.exception(msg)
            raise ShoppingListError(msg, ex)

    
class ViewResponseHelper(object):
    def set_response_headers(self, response, model_for_etag):
        # TODO response headers, content/mime type etc.: http://blog.nullobject.ca/2010/02/08/django-json-woes/
        # Paster sets these for us:
        # Content-Length:4780
        # Content-Type:application/json; charset=UTF-8
        
        # TODO X-XSS-Protection
        # TODO Fix headers....  Other cache headers
        # TODO Review date format?
        etag_model = EtagManager().get_etag_model(model_for_etag)
        response.headers['ETag'] = '"{0}"'.format(etag_model.etag)

        # Use etag last modified (so it includes last_modified of items)
        response.headers['Last-Modified'] = '{0}'.format(etag_model.last_modified)

        # TODO Ensure web server is setting Date
        # Server date
        #response.headers['Date'] = '{0}'.format(datetime.utcnow())

        # Allow caching only in the browser. Always require validation with server (must-revalidate).
        response.headers['Cache-Control'] = 'private, max-age=0, must-revalidate'
        response.headers['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'

        # Mask the true server, avoid showing: Apache/2.2.17 (Unix) mod_wsgi/3.3 Python/2.7.1 mod_ssl/2.2.17 OpenSSL/0.9.8o
        # (The value 'Server' is what www.amazon.com uses.)
        # TODO Alter the Server value in the web server config
        #response.headers['Server'] = 'Server'




    def create_json_http_response(self, json_content, status_int=httplib.OK):
        status = HttpResponseHelper.get_status_str(status_int)
        return Response(body=json_content, status=status, content_type=JsonHelper.JSON_CONTENT_TYPE, charset='UTF-8')

    def create_serialized_json_response(self, resource_data, shopping_list_model, include_etag_headers=False):
        """
        resource_data: dict or array representing the resource to serialize.
        """
        json_data = JsonHelper.serialize_to_json(resource_data)
        # 200 OK
        response = self.create_json_http_response(json_data)
        if include_etag_headers:
            self.set_response_headers(response, shopping_list_model)
        return response

    def create_empty_ok_response(self):
        return Response()

    def create_response_no_body(self, status_int=httplib.OK):
        # For 304 and 405, be careful not to set the content type (it's set by default in the webob Response ctor).
        # (If you want to see some bad code, review webob Response.py.)
        # If content is set on a request that shouldn't have it (e.g. 304) webtest will raise the error:
        #   File "build\bdist.win32\egg\webtest\lint.py", line 415, in check_content_type
        #   AssertionError: Content-Type header found in a 304 response, which must not return content.
        status = HttpResponseHelper.get_status_str(status_int)
        response = Response(status=status)
        # Erase the Content-Type and Content-Length headers that shouldn't be there.
        response.headerlist = []
        return response

    def create_response_not_allowed(self, allowed_methods):
        response = self.create_response_no_body(httplib.METHOD_NOT_ALLOWED)
        header_list = [('Allow', ','.join(allowed_methods))]
        response.headerlist = header_list
        return response

    def create_response_not_modified(self):
        return self.create_response_no_body(httplib.NOT_MODIFIED)