from pyramid.config import Configurator
from mcshoppinglist.auth.authentication import AuthenticationPolicy, AuthorizationPolicy
from mcshoppinglist.shared.mongodb import MongoManager
from mcshoppinglist.shared.requestdata import RequestSingleton
from mcshoppinglist.wsgiapp.resources import Root
from mcshoppinglist.wsgiapp.routes import add_url_dispatch_routes

def wsgimain(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    authentication_policy = AuthenticationPolicy()
    authorization_policy = AuthorizationPolicy()
    config = Configurator(root_factory=Root, settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)
    add_url_dispatch_routes(config)

    return config.make_wsgi_app()