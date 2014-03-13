import logging
from agents.behaviors import _get_all_behaviors

__author__ = 'john'


class BehaviorFactory:
    def __init__(self, behaviors=None):
        """
        :type behaviors: list[BaseBehavior]
        """
        eff_behaviors = behaviors if behaviors else _get_all_behaviors()
        self._behaviors_map = {behavior.behavior_key(): behavior for behavior in eff_behaviors}

    def register_behavior(self, key, factory_method):
        self._behaviors_map[key] = factory_method

    def create_behavior(self, key, *args, **kwargs):
        if key not in self._behaviors_map:
            msg = "Unknown behavior {key}".format(key)
            logger = logging.getLogger(__name__)
            logger.error(msg)
            raise ValueError(msg)

        return self._behaviors_map[key](*args, **kwargs)
