try:
    # noinspection PyShadowingBuiltins,PyUnresolvedReferences
    from itertools import ifiliter as filter
except ImportError:
    pass

__author__ = 'e.kolpakov'


class GoalDrivenBehaviorMixin:
    def __init__(self, backup_behavior, **kwargs):
        # noinspection PyArgumentList
        super(GoalDrivenBehaviorMixin, self).__init__(**kwargs)
        self._backup_behavior = backup_behavior

    def find_goal_handlers(self, goals, behavior_interface):
        try:
            yield from filter(lambda goal: isinstance(goal, behavior_interface), goals)
        except StopIteration:
            return self._backup_behavior

    def get_behavior_result(self, student, behavior_interface, *args, **kwargs):
        handlers = self.find_goal_handlers(student, behavior_interface)
        for handler in handlers:
            result = self.call_handler_method(handler, *args, **kwargs)
            return result
        return None

    def call_handler_method(self, handler, *args, **kwargs):
        raise NotImplemented