class AuthenticationDao(object):
    def __init__(self, authdb):
        """
        authdb: an already connected authentication Database from pymongo.
        """
        self.authdb = authdb

    def get_userid(self, login_token, remote_addr):
        # TODO impl
        return 'TEST_USER'
