import json
import datetime
from shoppinglists.exceptions import EncodingError
from django.utils import datetime_safe

class DateTimeEncoder(json.JSONEncoder):
    # Adapted from Django source: django\core\serializers\json.py
    #
    # This format conforms to the semi-standard JSON date format, particularly ISO 8601:
    # "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
    #
    # http://docs.python.org/library/datetime.html#strftime-strptime-behavior
    # http://download.oracle.com/javase/1.5.0/docs/api/java/text/SimpleDateFormat.html
    # http://weblogs.asp.net/bleroy/archive/2008/01/18/dates-and-json.aspx
    # http://www.w3.org/TR/NOTE-datetime
    # http://download.oracle.com/javase/1.5.0/docs/api/java/text/DateFormat.html
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
    TIME_FORMAT = "%H:%M:%S"

    def is_datetime_type(self, obj):
        return isinstance(obj, datetime.datetime) \
            or isinstance(obj, datetime.date) \
            or isinstance(obj, datetime.time) 
#            or isinstance(obj, decimal.Decimal)

    def encode_datetime(self, obj):
        if not self.is_datetime_type(obj):
            raise EncodingError('Object is not an allowed datetime type.')
        if isinstance(obj, datetime.time):
            # TODO When no date is specified, what should we return?
            return obj.strftime(self.TIME_FORMAT)
        if isinstance(obj, datetime.datetime):
            d = datetime_safe.new_datetime(obj)
        elif isinstance(obj, datetime.date):
            d = datetime_safe.new_date(obj)
#        elif isinstance(obj, decimal.Decimal):
#            return str(obj)
        else:
            raise EncodingError('Object is not an allowed datetime type (date/datetime).')
        return d.strftime(self.DATETIME_FORMAT)

    def default(self, obj):
        if self.is_datetime_type(obj):
            return self.encode_datetime(obj)
        return json.JSONEncoder.default(self, obj)


#class ObjMemberJsonEncoder(json.JSONEncoder):
#    """
#    Encode objects of any type to a nested dict { } representation compatible with the JSON serializer.
#    e.g. for obj: { "name": obj.name, "checked": obj.checked, "map": obj.map }
#    """
#    _datetime_encoder = DateTimeEncoder()
#
#    # TODO Enabling the below ctor results in this error:
#    #
#    #   File "C:\opt\python\Python27\lib\json\__init__.py", line 238, in dumps
#    #   **kw).encode(obj)
#    #   TypeError: __init__() got an unexpected keyword argument 'indent'
#    #
##    def __init__(self):
##        json.JSONEncoder.__init__(self)
##        self._datetime_encoder = DateTimeEncoder()
#
#    def _is_iterable(self, obj):
#        return InspectHelper.isiterable(obj)
#
#    def _has_dict(self, obj):
#        # http://docs.python.org/reference/datamodel.html
#        # __dict__ alone does not cover new-style classes that use __slots__
#        # TODO Adding or hasattr(obj, '__slots__') then how to get the members? Adding __slots__ includes Decimal, which should be instead handled via str()
#        return hasattr(obj, '__dict__') or InspectHelper.isdict(obj)
#
#    # TODO Cycle detection
#    def _encode(self, obj, remainingRecursionDepth):
#        if remainingRecursionDepth < 0:
#            return
#        remainingRecursionDepth -= 1
#
#        #json_value = None
#        if self._has_dict(obj):
#            # It's an object or dict
#            # represent in JSON as { key: value }
#            map = {}
#            obj_is_dict = InspectHelper.isdict(obj)
#            if obj_is_dict:
#                keys = obj.keys()
#            else:
#                #keys = obj.__dict__.keys()
#                keys = vars(obj)
#
#            for key in keys:
#                if not key:
#                    continue
#                if obj_is_dict:
#                    value = obj[key]
#                else:
#                    value = getattr(obj, key)
#                map[key] = self._encode(value, remainingRecursionDepth)
#            json_value = map
#        elif self._is_iterable(obj):
#            # It's a list or iterable, represent in JSON as (value1, value2)
#            items = []
#            for item in obj:
#                newItem = self._encode(item, remainingRecursionDepth)
#                if newItem:
#                    items.append(newItem)
#            json_value = items
#        else:
#            if self._datetime_encoder.is_datetime_type(obj):
#                # It's a datetime/date/time? Apply datetime formatting, return a string.
#                json_value = self._datetime_encoder.encode_datetime(obj)
#            else:
#                # It's a primitive? Leave it as raw type.
#                json_value = obj
#        return json_value
#
#
#
#    def default(self, obj):
#        """
#        returns: a nested dict { } representation of obj compatible with the JSON serializer.
#        e.g. { "name": obj.name, "checked": obj.checked, "map": obj.map }
#        """
#        if self._has_dict(obj):
#            return self._encode(obj, 16)
#        if obj and issubclass(obj.__class__, decimal.Decimal):
#            # TODO Is this conversion of Decimal to str valid?
#            return str(obj)
#        return json.JSONEncoder.default(self, obj)
#
#
#
#
## Not a json.JSONDecoder
#class ObjMemberInflator:
#    TYPE_PROPERTY = 'type'
#
#    def __init__(self, type_resolver=None):
#        """
#        type_resolve: TypeResolver implementation with resolve(class_name) => classobj method.
#        """
#        self.type_resolver = type_resolver
#
#    def _instantiate(self, class_name):
#        if not self.type_resolver:
#            raise EncodingException('Missing type resolver for object type: %s' % class_name)
#        try:
#            type_classobj = self.type_resolver.resolve(class_name)
#            # instantiate it
#            return type_classobj()
#        except:
#            raise EncodingException('Failed to get required type: %s   Cause: %s' % (class_name, sys.exc_info()))
#
#    def inflate(self, source_obj_dict):
#        """
#        Recursively inflate an object hierarchy from dict keys/values.
#
#        obj_dict: dict whose keys are members to set on an object.
#        The "type" key is used to determine the class. If it's not specified,
#        leave it as a dict but inflate its values.
#        """
#        if not InspectHelper.isdict(source_obj_dict):
#            raise EncodingException('No keys() or getitem found on object.')
#        keys = None
#        try:
#            keys = source_obj_dict.keys()
#        except:
#            raise EncodingException('Failed to get keys() from object: %s' % sys.exc_info())
#
#        typestr = None
#        try:
#            # Avoid the need for has_key or key in dict
#            typestr = source_obj_dict[ObjMemberInflator.TYPE_PROPERTY]
#        except:
#            # Ignore
#            pass
#
#        container_obj = {}
#        container_is_dict = True
#        if typestr:
#            container_is_dict = False
#            container_obj = self._instantiate(typestr)
#
#        for key in keys:
#            value = source_obj_dict[key]
#            if container_is_dict:
#                # __setitem__
#                container_obj[key] = value
#            else:
#                setattr(container_obj, key, value)
#
#
#
#def _run_tests():
#    print 'TEST: ' + __name__
#
#    # http://docs.python.org/library/datetime.html#strftime-strptime-behavior
#    # datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
#    SHARED_DATETIME = datetime.datetime(2011, 02, 15, 21, 15, 38)
#
#    class MySmallObj:
#        def __init__(self, name='unknown'):
#            self.name = name
#            self.lastmodified = SHARED_DATETIME
#            self.type = 'MySmallObj'
#
#    class MyTestClass:
#        def __init__(self):
#            self.str_var = "str value"
#            self.list_var = ['one', 'two', 'three']
#            self.list_objs_var = [ MySmallObj('obj1'), MySmallObj('obj2'), ]
#            self.dict_var = { 'one': 'val1d', 'two': 'val2d'}
#            self.dic_objs_var = { 'one': MySmallObj('obj1d'), 'two': MySmallObj('obj2d')}
#            self.datetime_var = SHARED_DATETIME
#            self.bool_var = True
#            self.double_var = 1.000888
#            self.decimal_var = decimal.Decimal('1008.0034181451667708')
#            self.type = 'MyTestClass'
#
#
#    # Encode to JSON
#    testObj = MyTestClass()
#    actual_json_data = json.dumps(testObj, ensure_ascii=False)
#    print 'Encoded to JSON string: ' + str(actual_json_data)
#    expected = '{"list_var": ["one", "two", "three"], "decimal_var": "1008.0034181451667708", "str_var": "str value", "dict_var": {"two": "val2d", "one": "val1d"}, "list_objs_var": [{"lastmodified": "2011-02-15T21:15:38", "type": "MySmallObj", "name": "obj1"}, {"lastmodified": "2011-02-15T21:15:38", "type": "MySmallObj", "name": "obj2"}], "datetime_var": "2011-02-15T21:15:38", "dic_objs_var": {"two": {"lastmodified": "2011-02-15T21:15:38", "type": "MySmallObj", "name": "obj2d"}, "one": {"lastmodified": "2011-02-15T21:15:38", "type": "MySmallObj", "name": "obj1d"}}, "double_var": 1.000888, "type": "MyTestClass", "bool_var": true}'
#    if actual_json_data != expected:
#        raise Exception('Failed to encode. Expected: ' + expected + '  Actual: ' + actual_json_data)
#
#    # Decode from JSON
#    actual_dict = json.loads(actual_json_data)
#    dict = globals()
#    dict['MyTestClass'] = MyTestClass().__class__
#    dict['MySmallObj'] = MySmallObj().__class__
#    type_resolver = SpecifiedTypeResolver(dict)
#    inflator = ObjMemberInflator(type_resolver)
#    inflated_obj = inflator.inflate(actual_dict)
#    print 'SUCCESS.'
#
#if __name__ == "__main__":
#    _run_tests()
#
