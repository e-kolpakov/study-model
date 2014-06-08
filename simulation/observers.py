from functools import wraps
from pubsub import pub

__author__ = 'e.kolpakov'


observer_attr = "observer"


def _append_observer(target, observer):
    """
    :param target: callable
    :param observer: BaseObserver
    """
    if not hasattr(target, observer_attr):
        setattr(target, observer_attr, [])
    observers = getattr(target, observer_attr)
    observers.append(observer)


def get_observers(target):
    """
    Gets observer attached to callable, if any
    :param target: callable
    :return: BaseObserver
    """
    return getattr(target, observer_attr) if hasattr(target, observer_attr) else []


class BaseObserver:
    def __init__(self, topic, target, converter=None):
        self._topic = topic
        self._target = target
        self._converter = converter if converter else lambda x: x

    def inspect(self, agent, step_number):
        raise NotImplementedError()

    def _get_value(self, agent):
        return self._converter(self._target(agent))


class Observer(BaseObserver):
    def __init__(self, topic, target, converter=None):
        super(Observer, self).__init__(topic, target, converter)

    def inspect(self, agent, step_number):
        pub.sendMessage(self._topic, agent=agent, value=self._get_value(agent), step_number=step_number)

    @classmethod
    def observe(cls, topic, converter=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            _append_observer(wrapper, cls(topic, func, converter))
            return wrapper
        return decorator


class DeltaObserver(BaseObserver):
    def __init__(self, topic, target, converter=None, delta_calculator=None):
        super(DeltaObserver, self).__init__(topic, target, converter)
        self._delta_calculator = delta_calculator
        self._previous = dict()

    def inspect(self, agent, step_number):
        value = self._get_value(agent)
        previous = self._get_previous_value(agent)
        delta = self._delta_calculator(value, previous) if previous is not None else value
        self._set_previous_value(agent, value)
        pub.sendMessage(self._topic, agent=agent, delta=delta, step_number=step_number)

    def _get_previous_value(self, agent):
        return self._previous[agent] if agent in self._previous else None

    def _set_previous_value(self, agent, value):
        self._previous[agent] = value

    @classmethod
    def observe(cls, topic, converter=None, delta=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            _append_observer(wrapper, cls(topic, func, converter, delta))
            return wrapper
        return decorator