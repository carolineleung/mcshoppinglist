import settings
from shoppinglists.exceptions import TracebackHelper, TracedError
from shoppinglists.helpers import JsonHelper

class JsonErrorFactory(object):
    ERROR_CODE_NONE = 'None'
    ERROR_CODE_UNHANDLED_EXCEPTION = 'UnhandledException'
    CODE_KEY = 'code'
    MESSAGE_KEY = 'message'
    TRACE_SHALLOW_KEY = 'trace_shallow'
    TRACE_DEEP_KEY = 'trace_deep'

    @staticmethod
    def _conditionally_add_tracebacks(json_dict, exception_cause):
        try:
            # Do not include stack traces in production.
            if settings.DEBUG:
                try:
                    json_dict[JsonErrorFactory.TRACE_SHALLOW_KEY] = TracebackHelper.get_traceback_str()
                except:
                    pass
                try:
                    if exception_cause and hasattr(exception_cause, TracedError.TRACEBACK_STR_MEMBER):
                        json_dict[JsonErrorFactory.TRACE_DEEP_KEY] = getattr(
                            exception_cause, TracedError.TRACEBACK_STR_MEMBER)
                except:
                    pass
        except:
            # Ignore
            pass

    @staticmethod
    def create_json_error_object(error_code=ERROR_CODE_NONE, error_message=None, exception_cause=None):
        if not error_message:
            error_message = ''
            if exception_cause:
                try:
                    if hasattr(exception_cause, TracedError.MESSAGE_MEMBER):
                        error_message += getattr(exception_cause, TracedError.MESSAGE_MEMBER, '')
                    else:
                        error_message += exception_cause.message
                except:
                    # ignore
                    pass
        json_dict = {
            # TODO Include requested resource? Request ID?
            # http://docs.amazonwebservices.com/AmazonS3/latest/dev/UsingRESTError.html
            JsonErrorFactory.CODE_KEY: error_code,
            JsonErrorFactory.MESSAGE_KEY: error_message
        }
        JsonErrorFactory._conditionally_add_tracebacks(json_dict, exception_cause)
        return json_dict

    @staticmethod
    def create_json_error_str(error_code=ERROR_CODE_NONE, error_message=None, exception_cause=None):
        try:
            json_dict = JsonErrorFactory.create_json_error_object(error_code, error_message, exception_cause)
            return JsonHelper.serialize_to_json(json_dict)
        except:
            # TODO log
            # Return an empty string since we failed to serialize the error.
            # (Don't want to rethrow when exception handling.)
            return ''