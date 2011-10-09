import httplib

# http://docs.python.org/tutorial/errors.html
import string
import sys
import traceback

class TracebackHelper(object):
    @staticmethod
    def get_traceback_str():
        if not sys.exc_info():
            return ''
        traceback_str = traceback.format_tb(sys.exc_info()[2], 100)
        if not traceback_str:
            return ''
        return string.join(traceback_str, '\n')

class TracedError(Exception):
    # Constants for member inspection.
    MESSAGE_MEMBER = 'message'
    INNER_EXCEPTION_MEMBER = 'inner_exception'
    TRACEBACK_STR_MEMBER = 'traceback_str'

    def _grab_self_traceback(self):
        tracebacks = ''
        try:
            tracebacks += TracebackHelper.get_traceback_str()
        except:
            # Ignore
            pass
        return tracebacks

    def __init__(self, message='', inner_exception=None):
        Exception.__init__(self)
        self.message = message
        self.inner_exception = inner_exception
        # TODO Is it dangerous to store the traceback as a string in the exception? e.g. out of memory condition.
        # 'Get the traceback as a str from the time the exception was thrown.'
        self.traceback_self_str = self._grab_self_traceback()
        self._cached_traceback_str = None

    def _get_traceback_str(self):
        if self._cached_traceback_str:
            return self._cached_traceback_str

        tracebacks = ''
        try:
            line_format = '{0}\n'
            # TODO This starts the traceback with the latest trace, rather than with the message.
            current_traceback = TracebackHelper.get_traceback_str()
            if current_traceback:
                tracebacks += line_format.format(current_traceback)
            current_ex = self
            depth = 0
            while current_ex and depth < 10:
                if current_ex and hasattr(current_ex, TracedError.MESSAGE_MEMBER):
                    tracebacks += line_format.format(getattr(current_ex, TracedError.MESSAGE_MEMBER, ''))
                if current_ex and hasattr(current_ex, 'traceback_self_str'):
                    tracebacks += line_format.format(getattr(current_ex, 'traceback_self_str', ''))
                depth += 1
                if hasattr(current_ex, TracedError.INNER_EXCEPTION_MEMBER):
                    current_ex = getattr(current_ex, TracedError.INNER_EXCEPTION_MEMBER)
        except:
            # ignore
            pass
        self._cached_traceback_str = tracebacks
        return tracebacks

    traceback_str = property(_get_traceback_str, doc='Return traceback as a string.')

    def __unicode__(self, *args, **kwargs):
        try:
            return self.traceback_str
        except:
            try:
                return self.message
            except:
                return ''

class ShoppingListError(TracedError):
    def __init__(self, *args, **kwargs):
        TracedError.__init__(self, *args, **kwargs)

class EncodingError(ShoppingListError):
    def __init__(self, *args, **kwargs):
        ShoppingListError.__init__(self, *args, **kwargs)

# Avoid using django's built in HTTP error responses (e.g. HttpResponseNotFound) in case we abandon django.
class HttpResponseError(ShoppingListError):
    # Member constants for use externally with hasattr on instances of this class.
    STATUS_CODE_MEMBER = 'status_code'
    MESSAGE_MEMBER = TracedError.MESSAGE_MEMBER
    INNER_EXCEPTION_MEMBER = TracedError.INNER_EXCEPTION_MEMBER

    def __init__(self, message='', status_code=httplib.INTERNAL_SERVER_ERROR, inner_exception=None):
        """
        status_code: HTTP status code int from httplib.
        """
        ShoppingListError.__init__(self, message, inner_exception)
        self.status_code = status_code
        try:
            if self.status_code:
                '({0}) {1}'.format(self.status_code, ShoppingListError.message)
        except:
            # ignore
            pass

