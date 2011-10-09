import json
import logging
from shoppinglists.encoders import DateTimeEncoder

logger = logging.getLogger(__name__)

class ClassHelper(object):
    @staticmethod
    def safe_issubclass_obj(obj, classinfo):
        if obj:
            return issubclass(obj.__class__, classinfo)
        return False

class InspectHelper(object):
    @staticmethod
    def isdict(obj):
        return hasattr(obj, 'keys') and hasattr(obj, '__getitem__')

    @staticmethod
    def isdictrw(obj):
        return hasattr(obj, 'keys') and hasattr(obj, '__getitem__') and hasattr(obj, '__setitem__')

    @staticmethod
    def isiterable(obj):
        return hasattr(obj, '__iter__')

class JsonHelper(object):
    # TODO content_type='application_json' can we get this from somewhere else? http://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/
    # TODO Should mimetype always include charset? application/json; charset=utf-8
    JSON_CONTENT_TYPE = 'application/json'

    @staticmethod
    def serialize_to_json(resource_dict):
        """
        returns: string
        """
        # ensure_ascii=False : unicode (not str)
        return json.dumps(resource_dict, ensure_ascii=False, cls=DateTimeEncoder)

    @staticmethod
    def deserialize_from_json(json_data_str):
        """
        returns: dict
        """
        return json.loads(json_data_str)

