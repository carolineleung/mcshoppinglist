from mcshoppinglist.auth.dao import AuthenticationDao
from mcshoppinglist.shared.logfactory import LogFactory
from mcshoppinglist.shared.mongodb import MongoManager

logger = LogFactory.get_logger(__name__)

class RequestSingleton(object):
    """
    An object that acts as a singleton for the duration of the request.
    """

    # Attribute name on the Request that we'll store this object in.
    REQUEST_DATA_ATTR_NAME = 'reqdata'

    def __init__(self, request):
        """
        request: a Request object, with .settings
        """
        if (hasattr(request, RequestSingleton.REQUEST_DATA_ATTR_NAME)
            and getattr(request, RequestSingleton.REQUEST_DATA_ATTR_NAME)):
            logger.warn('Prevented attempt to reinitialize request singleton.')
            return

        # http://docs.pylonsproject.org/projects/pyramid/1.0/whatsnew-1.0.html
        mongo = MongoManager(request.registry.settings)
        mongo.connect()
        self._mongo_manager = mongo

        # TODO This seems ugly...
        # Stash this object on the request
        setattr(request, RequestSingleton.REQUEST_DATA_ATTR_NAME, self)

    def create_authentication_dao(self):
        return AuthenticationDao(self._mongo_manager.authdb)

    def dispose(self):
        self._mongo_manager.disconnect()

    mongo_manager = property(lambda self: self._mongo_manager)