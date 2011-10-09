import httplib
from webob.response import Response
from mcshoppinglist.api.views.helpers import ViewResponseHelper
from mcshoppinglist.auth.authentication import AuthenticationManager

# TODO Move this
ORIGIN_COOKIE_NAME = 'origin'

class LoginView(object):
    def __init__(self):
        self.auth_mgr = AuthenticationManager()

    def login_interstitial1(self, request):
        # TODO Impl properly
        if request.method == 'POST':
            resp_helper = ViewResponseHelper()
            response = resp_helper.create_response_no_body(status_int=httplib.FOUND)
            self.auth_mgr.set_login_cookie(response, self.auth_mgr.create_login_token())
            # TODO Redirect to original location prior to login interstitial

            origin = '/'
            if ORIGIN_COOKIE_NAME in request.cookies:
                origin_cookie = request.cookies[ORIGIN_COOKIE_NAME]
                # TODO Check hostname matches request hostname using request.environ['HTTP-HOST']
                if origin_cookie:
                    origin = origin_cookie

            response.headers['Location'] = str(origin)
            return response
        
        # else
        return {
            'static_content_path': '/static' # TODO Push this out to settings/config file.
        }

    def login_api_login(self, request):
        return Response()



def login_empty_interstitial1(request):
    return {
        'static_content_path': '/static' # TODO Push this out to settings/config file.
    }

def login_interstitial1(request):
    return LoginView().login_interstitial1(request)

def login_api_login(request):
    return LoginView().login_api_login(request)

def login_redirect(request):
    # TODO Impl properly
    response = Response(status=httplib.FOUND)
    response.headers['Location'] = str('{0}/login/'.format(request.application_url))
    # TODO May need to encode the URL for special chars?
    response.set_cookie(ORIGIN_COOKIE_NAME, '{0}'.format(request.url), max_age=60*3, path='/')
    return response