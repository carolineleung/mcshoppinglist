import mongoengine
from mcshoppinglist.shared.exceptions import ShoppingListError
from pymongo import Connection

class MongoManager(object):
    SETTING_MONGODB_PRIMARY_NAME = 'mongodb_name'
    SETTING_MONGODB_AUTH_NAME = 'mongodb_auth_name'
    MONGODB_CONNECTION_TIMEOUT_S = 10

    def __init__(self, settings):
        """
        settings: Pyramid settings dict
        """
        self._settings = settings

    def _raise_setting_error(self, setting_name):
        raise ShoppingListError('Invalid/missing mongodb setting: {0}'.format(setting_name))

    def _get_setting(self, settings, setting_name):
        if not setting_name in settings:
            self._raise_setting_error(setting_name)
        setting_value = settings[setting_name]
        if not setting_value:
            self._raise_setting_error(setting_name)
        return setting_value

    def connect(self):
        self._connect_to_primary_db(self._settings)
        self._connect_to_auth_db(self._settings)

    def disconnect(self):
        try:
            self._primary_db.connection.disconnect()
        except Exception as ex:
            pass
        try:
            self._authdb.connection.disconnect()
        except Exception as ex:
            pass

    def _connect_to_primary_db(self, settings):
        """
        settings: a dictionary of mongodb configuration settings.
        """
        db_name = self._get_setting(settings, MongoManager.SETTING_MONGODB_PRIMARY_NAME,)
        
        # TODO Other MongoDB settings (host, port, etc.)

        # MongoDB MongoEngine
#        self._primary_db = mongoengine.connect(db_name, host='localhost', port=27017)
        self._connection_primary_db = Connection('localhost', 27017,
                                             network_timeout=MongoManager.MONGODB_CONNECTION_TIMEOUT_S)
        self._primary_db =self._connection_primary_db[db_name]


    def _connect_to_auth_db(self, settings):
        """
        settings: a dictionary of mongodb configuration settings.
        """
        db_name = self._get_setting(settings, MongoManager.SETTING_MONGODB_AUTH_NAME)

        # TODO Other MongoDB settings (host, port, etc.)

        # MongoDB pymongo
        self._connection_authdb = Connection('localhost', 27017,
                                             network_timeout=MongoManager.MONGODB_CONNECTION_TIMEOUT_S)
        self._authdb = self._connection_authdb[db_name]

    def _get_authdb(self):
        if not self._authdb:
            raise ShoppingListError('Not connected to (auth) db.')
        return self._authdb

    authdb = property(_get_authdb)
