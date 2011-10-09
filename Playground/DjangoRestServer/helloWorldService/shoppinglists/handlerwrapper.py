import httplib
import logging
from django.http import HttpResponse
from shoppinglists.apierrors import JsonErrorFactory
from shoppinglists.exceptions import HttpResponseError, ShoppingListError
from shoppinglists.helpers import JsonHelper

logger = logging.getLogger(__name__)

class RequestHandlerWrapper(object):
    @staticmethod
    def handle(callable, *args, **kwargs):
        """
        returns: django HttpResposne
        """
        try:
            # * unpacks argument list: http://docs.python.org/tutorial/controlflow.html
            return callable(*args, **kwargs)
        except Exception as ex:
            try:
                # Include ex in case it's one of our own exceptions that overrides __unicode__
                logger.exception('Request handler caught an exception: {0}\n{1}\n'.format(ex.message, ex))
            except:
                # Ignore logger errors
                pass

            content = ''
            # Unhandled exceptions become 500 Internal server error unless the exception specifies the status_code.
            status_code = httplib.INTERNAL_SERVER_ERROR
            error_code = JsonErrorFactory.ERROR_CODE_UNHANDLED_EXCEPTION
            message = ''
            # If the exception has additional information such as a message
            # or an HTTP status code (e.g. HttpResponseException),
            # include that information in the HttpResponse.
            try:
                # TODO Change error_code to be more indicative (e.g. 404)
                if hasattr(ex, HttpResponseError.STATUS_CODE_MEMBER):
                    status_code = getattr(ex, HttpResponseError.STATUS_CODE_MEMBER, status_code)
            except:
                #ignore
                pass

            # Convert the error message to a JSON response.
            try:
                content = JsonErrorFactory.create_json_error_str(error_code, message, ex)
            except:
                # Ignore
                pass

            # HttpResponse: def __init__(self, content='', mimetype=None, status=None, content_type=None):
            return HttpResponse(content=content, status=status_code, content_type=JsonHelper.JSON_CONTENT_TYPE)
