__author__ = 'john'


class ResultRecord(object):
    def __init__(self, key, timestamp, value):
        self._key = key
        self._timestamp = timestamp
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def value(self):
        return self._value
