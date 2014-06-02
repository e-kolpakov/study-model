from functools import wraps
from pubsub import pub

__author__ = 'e.kolpakov'


observer_attr = "observer"

def _set_scheduler(target, observer):
    """
    :param target: callable
    :param observer: BaseObserver
    """
    setattr(target, observer_attr, observer)


def get_observer(target):
    """
    Gets observer attached to callable, if any
    :param target: callable
    :return: BaseObserver
    """
    return getattr(target, observer_attr) if hasattr(target, observer_attr) else None


class BaseObserver:
    def __init__(self, topic, target, converter=None):
        self._topic = topic
        self._target = target
        self._converter = converter if converter else lambda x: x

    def observe(self, step_number):
        agent = self._target.__self__
        value = self._converter(self._target())
        pub.sendMessage(self._topic, agent=agent, value=value, step_number=step_number)


class DeltaObserver(BaseObserver):
    def __init__(self, topic, target, converter=None, delta_calculator=None):
        super(DeltaObserver, self).__init__(topic, target, converter)
        self._delta_calculator = delta_calculator
        self._previous = None

    def observe(self, step_number):
        agent = self._target.__self__
        value = self._converter(self._target())
        delta = self._delta_calculator(value, self._previous) if self._previous is not None else value
        pub.sendMessage(self._topic, agent=agent, delta=delta, step_number=step_number)


def observe(topic, converter=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        _set_scheduler(wrapper, BaseObserver(topic, func, converter))
        return wrapper
    return decorator


def observe_delta(topic, converter=None, delta=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        _set_scheduler(wrapper, DeltaObserver(topic, func, converter, delta))
        return wrapper
    return decorator