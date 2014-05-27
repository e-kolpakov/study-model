from functools import wraps
import sys

__author__ = 'e.kolpakov'

scheduled_attr = "schedule"


def _set_scheduler(target, scheduler):
    """
    :param target: callable
    :param scheduler: BaseScheduler
    """
    setattr(target, scheduled_attr, scheduler)


def get_scheduler(target):
    """
    Gets scheduler attached to callable, if any
    :param target: callable
    :return: BaseScheduler
    """
    return getattr(target, scheduled_attr) if hasattr(target, scheduled_attr) else None


class BaseScheduler:
    def check_execution_condition(self, step_number):
        """
        Checks if execution condition is met
        :param step_number: int
        :rtype : bool
        """
        return True


class StepScheduler(BaseScheduler):
    def __init__(self, start=0, stop=sys.maxsize, step=1):
        self._start = start
        self._stop = stop
        self._step = step
        self._last_run = None

    def check_execution_condition(self, step_number):
        """
        Checks if execution condition is met
        :param step_number: int
        :rtype : bool
        """
        if step_number < self._start or step_number >= self._stop:
            return False

        last_run = self._last_run or 0
        if step_number != self._start and (step_number - last_run) % self._step != 0:
            return False

        self._last_run = step_number
        return True


def steps(start=0, stop=sys.maxsize, step=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        _set_scheduler(wrapper, StepScheduler(start, stop, step))
        return wrapper
    return decorator

