from abc import ABCMeta, abstractmethod

try:
    # noinspection PyShadowingBuiltins,PyUnresolvedReferences
    from itertools import ifiliter as filter
except ImportError:
    pass

__author__ = 'e.kolpakov'


class GoalDrivenBehaviorMixin(metaclass=ABCMeta):
    def __init__(self, backup_behavior, **kwargs):
        # noinspection PyArgumentList
        super(GoalDrivenBehaviorMixin, self).__init__(**kwargs)
        self._backup_behavior = backup_behavior

    def get_behavior_result(self, goals, behavior_interface, *args, **kwargs):
        target_goals = [goal for goal in goals if isinstance(goal, behavior_interface)]
        if not target_goals:
            return self.call_handler_method(self._backup_behavior, *args, **kwargs)
        results = {goal: self.call_handler_method(goal, *args, **kwargs) for goal in target_goals}
        return self.merge_goal_results(results)

    @abstractmethod
    def call_handler_method(self, handler, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def merge_goal_results(self, results):
        raise NotImplemented