try:
    from itertools import ifiliter as filter
except ImportError:
    pass

__author__ = 'e.kolpakov'


class GoalDrivenBehaviorMixin:
    def __init__(self, backup_behavior, **kwargs):
        super(GoalDrivenBehaviorMixin, self).__init__(**kwargs)
        self._backup_behavior = backup_behavior

    def find_goal_handler(self, student, behavior_interface):
        try:
            return next(filter(lambda goal: isinstance(goal, behavior_interface), student.goals))
        except StopIteration:
            return self._backup_behavior

