import datetime
import json

from decimal import Decimal
from numpy import long
import time


class JsonCustomEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        self.is_all = kwargs.pop('is_all', False)
        self.datetime_fmt = kwargs.pop('datetime_fmt', '%Y-%m-%d %H:%M:%S')
        self.date_fmt = kwargs.pop('date_fmt', '%Y-%m-%d')
        super().__init__(*args, **kwargs)

    @staticmethod
    def time_microsecond(date_time):
        if date_time:
            return long(time.mktime(date_time.timetuple()) * 1000000)
        return 0

    @staticmethod
    def time_millisecond(date_time):
        if date_time:
            return long(time.mktime(date_time.timetuple()) * 1000)
        return 0

    def default(self, field):
        if isinstance(field, datetime.datetime):
            if 'microsecond' == self.datetime_fmt:
                return self.time_microsecond(field)
            if 'millisecond' == self.datetime_fmt:
                return self.time_millisecond(field)
            return field.strftime(self.datetime_fmt)
            # return time.mktime(field.timetuple())*1000
        elif isinstance(field, datetime.date):
            return field.strftime(self.date_fmt)
        elif isinstance(field, Decimal):
            return str(field)
        elif isinstance(field, bytes):
            return field.decode()
        else:
            return json.JSONEncoder.default(self, field)


class AllJsonCustomEncoder(JsonCustomEncoder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_all = True


def to_dict(obj, is_all=False):
    """转化为dict is_all为True时不过滤字段"""
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return obj


def dict_to_str(ctx, **kwargs):
    if isinstance(ctx, (dict, list)):
        return json.dumps(ctx, cls=JsonCustomEncoder, skipkeys=True, ensure_ascii=False, **kwargs)

