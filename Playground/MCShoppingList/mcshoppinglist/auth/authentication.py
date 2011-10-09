from datetime import datetime
from mcshoppinglist.shared.requestdata import RequestSingleton

class AuthenticationManager(object):
    LOGIN_COOKIE_KEY = 'auth'
    LOGIN_DEFAULT_MAX_AGE_SECONDS = 1209600
    LOGIN_DEFAULT_PATH = '/'
    PERMISSION_ACCESS = 'access'

    def create_login_token(self):
        return 'TEST_LOGIN_TOKEN'

    def set_login_cookie(self, response, login_token):
        # TODO Set domain=top level domain so it applies to *.oursite.com
        response.set_cookie(AuthenticationManager.LOGIN_COOKIE_KEY,
                            login_token, max_age=AuthenticationManager.LOGIN_DEFAULT_MAX_AGE_SECONDS,
                            path=AuthenticationManager.LOGIN_DEFAULT_PATH)

    def _get_expires_str(self, max_age):
        future = datetime.datetime.utcnow() + datetime.timedelta(
                seconds=int(max_age))
        # Wdy, DD-Mon-YY HH:MM:SS GMT
        # Thu, 21-Mar-2013 18:23:11 GMT
        return future.strftime('%a, %d-%b-%Y %H:%M:%S GMT')

    def create_login_cookie_headers(self, login_token):
        # PREF=value; expires=Thu, 21-Mar-2013 18:23:11 GMT; path=/; domain=.google.ca
        cookie_value = '{0}={1}; path={2}; max-age={3}; expires={4}'.format(
            AuthenticationManager.LOGIN_COOKIE_KEY,
            login_token, AuthenticationManager.LOGIN_DEFAULT_PATH,
            AuthenticationManager.LOGIN_DEFAULT_MAX_AGE_SECONDS,
            self._get_expires_str(AuthenticationManager.LOGIN_DEFAULT_MAX_AGE_SECONDS))
        # See pyramid/authentication.py AuthTktCookieHelper
        return [ ('Set-Cookie', cookie_value)]

    def get_login_cookie(self, request):
        if not AuthenticationManager.LOGIN_COOKIE_KEY in request.str_cookies:
            return None
        return request.str_cookies[AuthenticationManager.LOGIN_COOKIE_KEY]

    def is_valid_login_token(self, login_token):
        return 'TEST_LOGIN_TOKEN' == login_token


class AuthenticationPolicy(object):
    """ An object representing a Pyramid authentication policy.

    See pyramid/authentication.py and interfaces.py
    Intentionally omitting this Zope interface junk: implements(IAuthenticationPolicy)
    Using duck type inheritance instead.
    """

    def authenticated_userid(self, request):
        """ Return the authenticated userid or ``None`` if no authenticated
        userid can be found. This method of the policy should ensure that a
        record exists in whatever persistent store is used related to the
        user (the user should not have been deleted); if a record associated
        with the current id does not exist in a persistent store, it should
        return ``None``."""
        auth_mgr = AuthenticationManager()
        login_token = auth_mgr.get_login_cookie(request)
        if not login_token:
            return None
        RequestSingleton(request)
        auth_dao = request.reqdata.create_authentication_dao()
        remote_addr = request.environ['REMOTE_ADDR']
        return auth_dao.get_userid(login_token, remote_addr)

    def unauthenticated_userid(self, request):
        """ Return the *unauthenticated* userid.  This method performs the
        same duty as ``authenticated_userid`` but is permitted to return the
        userid based only on data present in the request; it needn't (and
        shouldn't) check any persistent store to ensure that the user record
        related to the request userid exists."""
        return None

    def effective_principals(self, request):
        """ Return a sequence representing the effective principals
        including the userid and any groups belonged to by the current
        user, including 'system' groups such as Everyone and
        Authenticated. """
        from pyramid.security import Everyone, Authenticated
        import pyramid.authentication
        effective_principals = [Everyone]
        userid = self.authenticated_userid(request)
        if userid:
            effective_principals.append(userid)
            effective_principals.append(Authenticated)
        return effective_principals

    def remember(self, request, principal, **kw):
        """ Return a set of headers suitable for 'remembering' the
        principal named ``principal`` when set in a response.  An
        individual authentication policy and its consumers can decide
        on the composition and meaning of **kw. """
        # TODO impl?
        return []

    def forget(self, request):
        """ Return a set of headers suitable for 'forgetting' the
        current user on subsequent requests. """
        # TODO impl?
        return []

class AuthorizationPolicy(object):
    """ An object representing a Pyramid authorization policy.

    See pyramid/authentication.py and interfaces.py
    Intentionally omitting this Zope interface junk: implements(IAuthenticationPolicy)
    Using duck type inheritance instead.
    """
    def permits(self, context, principals, permission):
        """ Return ``True`` if any of the ``principals`` is allowed the
        ``permission`` in the current ``context``, else return ``False``
        """
        # TODO impl properly
        from pyramid.security import Authenticated
        allowed = len([x for x in principals if x == Authenticated]) > 0
        return allowed

    def principals_allowed_by_permission(self, context, permission):
        """ Return a set of principal identifiers allowed by the
        ``permission`` in ``context``.  This behavior is optional; if you
        choose to not implement it you should define this method as
        something which raises a ``NotImplementedError``.  This method
        will only be called when the
        ``pyramid.security.principals_allowed_by_permission`` API is
        used."""
        raise NotImplementedError('Not implemented. (principals_allowed_by_permission)')