__author__ = 'john'


class Observable(object):
    def __init__(self, key, nam=None):
        self._key = key
        self._name = name

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name if self._name else self.key
