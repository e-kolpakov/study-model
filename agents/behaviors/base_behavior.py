__author__ = 'john'

BEHAVIOR_TYPE = "Behavior"


class BaseBehavior:
    def __init__(self):
        pass

    @classmethod
    def behavior_key(cls):
        return BEHAVIOR_TYPE + "." + cls.__name__.replace(BEHAVIOR_TYPE, "")