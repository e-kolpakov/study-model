__author__ = 'john'


class BaseBehavior:
    def __init__(self):
        pass

    @classmethod
    def behavior_key(cls):
        return cls.__name__