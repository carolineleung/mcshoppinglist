from datetime import datetime

DEFAULT_DATE=datetime(2011, 01, 01)
INVALID_ID = -1

class ModelStateConstants(object):
    LIVE = 'LIVE'
    DELETED = 'DELETED'
    ALL_STATES = { LIVE, DELETED }

DEFAULT_STATE = ModelStateConstants.LIVE

