from functools import wraps
from pubsub import pub

__author__ = 'e.kolpakov'


def get_observers(target):
    """
    Gets observer attached to callable, if any
    :param target: callable
    :return: BaseObserver
    """
    return getattr(target, BaseObserver.OBSERVER_ATTRIBUTE) if hasattr(target, BaseObserver.OBSERVER_ATTRIBUTE) else []


class BaseObserver:
    OBSERVER_ATTRIBUTE = "observer"

    def __init__(self, topic, target):
        self._topic = topic
        self._target = target

    def inspect(self, agent, step_number):
        raise NotImplementedError()

    @staticmethod
    def _append_observer(target, observer):
        """
        :param target: callable
        :param observer: BaseObserver
        """
        if not hasattr(target, BaseObserver.OBSERVER_ATTRIBUTE):
            setattr(target, BaseObserver.OBSERVER_ATTRIBUTE, [])
        observers = getattr(target, BaseObserver.OBSERVER_ATTRIBUTE)
        observers.append(observer)


class Observer(BaseObserver):
    def __init__(self, topic, target, converter=None):
        super(Observer, self).__init__(topic, target)
        self._converter = converter if converter else lambda x: x

    def inspect(self, agent, step_number):
        pub.sendMessage(self._topic, agent=agent, step_number=step_number, value=self._get_value(agent))

    def _get_value(self, agent):
        return self._converter(self._target(agent))

    @property
    def topic(self):
        """
        :return: str
        """
        return self._topic

    @classmethod
    def observe(cls, topic, converter=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            cls._append_observer(wrapper, cls(topic, func, converter))
            return wrapper
        return decorator


class DeltaObserver(Observer):
    def __init__(self, topic, target, converter=None, delta_calculator=None):
        super(DeltaObserver, self).__init__(topic, target, converter)
        self._delta_calculator = delta_calculator
        self._previous = dict()

    def inspect(self, agent, step_number):
        value = self._get_value(agent)
        previous = self._get_previous_value(agent)
        delta = self._delta_calculator(value, previous) if previous is not None else value
        self._set_previous_value(agent, value)
        pub.sendMessage(self._topic, agent=agent, step_number=step_number, delta=delta)

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
            cls._append_observer(wrapper, cls(topic, func, converter, delta))
            return wrapper
        return decorator


class CallObserver(BaseObserver):
    @classmethod
    def observe(cls, topic):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                value = func(*args, **kwargs)
                pub.sendMessage(topic, arguments=args, kwargs=kwargs)
                return value
            return wrapper
        return decorator


class AgentCallObserver(BaseObserver):
    @classmethod
    def observe(cls, topic):
        from simulation.agents.base_agent import BaseAgent

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                value = func(*args, **kwargs)
                agent = args[0]
                if not isinstance(agent, BaseAgent):
                    raise ValueError("Base agent expected, got {0}", agent)
                step_number = agent.step_number
                pub.sendMessage(topic, agent=agent, step_number=step_number, args=args, kwargs=kwargs)
                return value
            return wrapper
        return decorator
