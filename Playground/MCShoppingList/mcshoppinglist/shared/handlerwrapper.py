import httplib
import logging
from pyramid.response import Response
from mcshoppinglist.api.apierrors import JsonErrorFactory
from mcshoppinglist.shared.exceptions import HttpResponseError
from mcshoppinglist.shared.helpers import HttpResponseHelper, JsonHelper
from mcshoppinglist.shared.logfactory import LogFactory
from mcshoppinglist.shared.mongodb import MongoManager
from mcshoppinglist.shared.requestdata import RequestSingleton

logger = LogFactory.get_logger(__name__)

# TODO Consider using a pyramid/pylons exception view: http://docs.pylonsproject.org/projects/pyramid/1.0/narr/views.html#using-special-exceptions-in-view-callables
class RequestHandlerWrapper(object):
    def handle_request(self, callable, request, *args, **kwargs):
        rs = None
        """
        callable: method to invoke
        request: Request object
        returns: django HttpResposne
        """
        try:
            rs = RequestSingleton(request)
            # * unpacks argument list: http://docs.python.org/tutorial/controlflow.html
            return callable(request, *args, **kwargs)
        except Exception as ex:
            try:
                # Include ex in case it's one of our own exceptions that overrides __unicode__
                logger.exception('Request handler caught an exception: {0}\n{1}\n'.format(ex.message, ex))
            except:
                # Ignore logger errors
                pass

            content = ''
            # Unhandled exceptions become 500 Internal server error unless the exception specifies the status.
            status_int = httplib.INTERNAL_SERVER_ERROR
            error_code = JsonErrorFactory.ERROR_CODE_UNHANDLED_EXCEPTION
            message = ''
            # If the exception has additional information such as a message
            # or an HTTP status code (e.g. HttpResponseError),
            # include that information in the HttpResponse.
            try:
                # TODO Change error_code to be more indicative (e.g. 404)
                if hasattr(ex, HttpResponseError.STATUS_INT_MEMBER):
                    status_int = getattr(ex, HttpResponseError.STATUS_INT_MEMBER, status_int)
            except:
                #ignore
                pass

            # Convert the error message to a JSON response.
            try:
                content = JsonErrorFactory.create_json_error_str(error_code, message, ex)
            except:
                # Ignore
                pass

            # TODO Consider using pyramid/pylons pyramid.httpexceptions.HTTPxxxxxxx exceptions (from webob).
            # http://docs.pylonsproject.org/projects/pyramid/1.0/api/httpexceptions.html

            status = HttpResponseHelper.get_status_str(status_int)
            # In pypramid/pylons, a webob.Response.
            return Response(body=content, status=status, content_type=JsonHelper.JSON_CONTENT_TYPE)
        finally:
            try:
                if rs:
                    rs.dispose()
            except Exception as ex:
                try:
                    logger.exception('Failed to dispose RequestSingleton / disconnect from mongodb. {0}'.format(ex))
                except:
                    pass

    @staticmethod
    def handle(callable, request, *args, **kwargs):
        wrapper = RequestHandlerWrapper()
        return wrapper.handle_request(callable, request, *args, **kwargs)
