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

    def __eq__(self, other):
        if not isinstance(other, ResultRecord):
            return False
        return other.key == self.key and other.timestamp == self.timestamp and other.value == self.value

    def __hash__(self):
        return hash(self.key) * 31**2 + hash(self.timestamp) * 31 + hash(self.value)
