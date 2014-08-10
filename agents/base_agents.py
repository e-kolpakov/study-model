from collections import defaultdict
from itertools import chain

from infrastructure.observers import BaseObserver


__author__ = 'e.kolpakov'


class BaseAgent:
    agent_count_by_type = defaultdict(int)

    def __init__(self, agent_id=None):
        actual_type = type(self)
        self.agent_count_by_type[actual_type] += 1
        self._agent_id = agent_id if agent_id else actual_type.__name__ + str(self.agent_count_by_type[actual_type])
        self._env = None
        self._observers_cache = None

    @property
    def agent_id(self):
        return self._agent_id

    @property
    def env(self):
        """
        :rtype: simpy.Environment
        """
        return self._env

    @env.setter
    def env(self, value):
        """
        :param value: simpy.Environment
        """
        self._env = value

    @property
    def time(self):
        return self.env.now

    def observe(self):
        for observer in self._get_all_observables():
            observer.inspect(self)

    def _get_all_observables(self):
        """
        :rtype: list[BaseObserver]
        """
        if not self._observers_cache:
            self._observers_cache = []
            candidates = chain(self._get_all_callables(), self._get_all_properties())
            for member in candidates:
                observers = self.get_observers(member)
                for observer in observers:
                    self._observers_cache.append(observer)
        return self._observers_cache

    def _get_all_callables(self):
        for member_name in dir(self.__class__):
            member = getattr(self, member_name)
            if callable(member):
                yield member

    def _get_all_properties(self):
        for member_name in dir(self.__class__):
            member = getattr(self.__class__, member_name)
            if isinstance(member, property):
                yield member.fget

    @staticmethod
    def get_observers(target):
        """
        Gets observer attached to callable, if any
        :param target: callable
        :return: BaseObserver
        """
        return getattr(target, BaseObserver.OBSERVER_ATTRIBUTE) if hasattr(target, BaseObserver.OBSERVER_ATTRIBUTE) else []


class IntelligentAgent(BaseAgent):
    pass


