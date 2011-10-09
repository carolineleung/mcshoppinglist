import json
from mcshoppinglist.shared.helpers import JsonHelper

class HttpTestClientWrapper(object):
    # TODO Are these defined somewhere? Don't see them in httlib (py2.7)
    HTTP_METHOD_GET='GET'
    HTTP_METHOD_POST='POST'
    HTTP_METHOD_PUT='PUT'
    HTTP_METHOD_DELETE='DELETE'

    def __init__(self, testapp):
        """
        testapp: a webtest TestApp for our WSGI application.
        """
        self.testapp = testapp
        # The URLs with Django client.get() must be relative to the project base (cannot be relative to url patterns in shoppinglists.urls)
        self.base_uri = '/api/v1/shoppinglists/'

    def _print_request_info(self, request_uri, http_method, request_body=None, etag_header=None):
        print '\n__________ REQUEST:\n'
        print '\n{0} {1}\n'.format(http_method, request_uri)
        if etag_header:
            print 'If-None-Match: {0}\n'.format(etag_header)
        if request_body:
            print '{0}\n'.format(request_body)

    def _print_response_info(self, response):
        print '__________ RESPONSE:  {0}\n'.format(response.status)
        try:
            json_obj = json.loads(response.body)
            pretty_json = json.dumps(json_obj, sort_keys=True, indent=4)
            print '{0}\n\n'.format(pretty_json)
        except Exception:
            print '{0}\n\n'.format(response.body)

    def create_relative_uri(self, uri_suffix=''):
        return '{0}{1}'.format(self.base_uri, uri_suffix)

    def _make_http_request_rel_uri(self, relative_uri, expected_status_int,
                                   http_method, request_body=None, etag_header=None):
        request_uri = self.create_relative_uri(relative_uri)
        self._print_request_info(request_uri, http_method, request_body, etag_header)
        if http_method == HttpTestClientWrapper.HTTP_METHOD_GET:
            if etag_header:
                headers = { 'If-None-Match': '"{0}"'.format(etag_header) }
                response = self.testapp.get(request_uri, headers=headers, status=expected_status_int)
            else:
                response = self.testapp.get(request_uri, status=expected_status_int)
        elif http_method == HttpTestClientWrapper.HTTP_METHOD_POST:
            response = self.testapp.post(request_uri, params=request_body, content_type=JsonHelper.JSON_CONTENT_TYPE)
        elif http_method == HttpTestClientWrapper.HTTP_METHOD_PUT:
            response = self.testapp.put(request_uri, params=request_body, content_type=JsonHelper.JSON_CONTENT_TYPE)
        else:
            raise Exception('Unimplemented method {0}'.format(http_method))

        self._print_response_info(response)
        # TODO This is now redundant because WebTest checks it for us.
        if response.status_int != expected_status_int:
            raise Exception('Expected status code: {0}   Actual: {1}'.format(expected_status_int, response.status_int))
        return response

    def get_rel_uri(self, relative_uri, expected_status_int, etag_header=None):
        """
        Make a get request to a URI relative to the API at /api/v1/shoppinglists/
        """
        return self._make_http_request_rel_uri(relative_uri, expected_status_int,
                                               HttpTestClientWrapper.HTTP_METHOD_GET, etag_header=etag_header)

    def put_rel_uri(self, relative_uri, expected_status_int, request_body):
        return self._make_http_request_rel_uri(relative_uri, expected_status_int,
                                               HttpTestClientWrapper.HTTP_METHOD_PUT, request_body)

    def post_rel_uri(self, relative_uri, expected_status_int, request_body):
        return self._make_http_request_rel_uri(relative_uri, expected_status_int,
                                               HttpTestClientWrapper.HTTP_METHOD_POST, request_body)

class EtagResponseDataSnapshot(object):
    def _assert_header(self, response, header_name, must_contain=None):
        self.asserter.assertTrue(header_name in response.headers,
                msg='Missing response header: {0}'.format(header_name))
        header_value = response.headers[header_name]
        self.asserter.assertTrue(len(header_value) > 0,
                msg='Empty response header: {0}'.format(header_name))
        if must_contain:
            self.asserter.assertTrue(header_value.find(must_contain) >= 0,
                'Failed to find str in response header. Expected to contain: "{0}" '
                'Actual: "{1}"     (Ignore quotes).'.format(must_contain, header_value))
        return header_value

    def __init__(self, response, test_case):
        self.asserter = test_case
        self.response = response

        # TODO Are the HTTP headers constants ETag etc. defined somewhere? http://docs.python.org/library/httplib.html
        self.etag = self._assert_header(response, 'ETag')
        self.last_modified = self._assert_header(response, 'Last-Modified')

        self._assert_header(response, 'Cache-Control')
        self._assert_header(response, 'Expires')

        # These will be set by the web server, so we don't assert them here.
        #self._assert_header(response, 'Date')
        #server = self._assert_header(response, 'Server')
        #self.asserter.assertTrue(server.find('Server') == 0)

        # TODO Add conditional asserts (when there's content in the response)
        #self._assert_header(response, 'Content-Type')
        #self._assert_header(response, 'Content-Encoding')
        #self._assert_header(response, 'Content-Length')


