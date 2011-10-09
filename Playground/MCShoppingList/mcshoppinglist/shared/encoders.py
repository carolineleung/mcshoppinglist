import json
from datetime import time, datetime, date
from mcshoppinglist.shared.exceptions import EncodingError

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
        # type() is only safe for new style classes, per http://docs.python.org/reference/datamodel.html
        return issubclass(type(obj), datetime) \
            or issubclass(type(obj), date)
#            or issubclass(obj, time)
#            or isinstance(obj, decimal.Decimal)

    def encode_datetime(self, obj):
        if not self.is_datetime_type(obj):
            raise EncodingError('Object is not an allowed datetime type.')
        d = obj
        # type() is only safe for new style classes, per http://docs.python.org/reference/datamodel.html
        if not issubclass(type(obj), datetime):
            if issubclass(type(obj), time):
                # TODO When no date is specified, what should we return?
                d = datetime.combine(date.min, obj)
            elif issubclass(type(obj), datetime.date):
                d = datetime.combine(obj, time(0))
            else:
                raise EncodingError('Object is not an allowed datetime type (date/datetime).')
        return d.strftime(self.DATETIME_FORMAT)

    def default(self, obj):
        if self.is_datetime_type(obj):
            return self.encode_datetime(obj)
        return json.JSONEncoder.default(self, obj)


