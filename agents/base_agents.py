from collections import defaultdict
from itertools import chain

from infrastructure.observers import BaseObserver, get_observers


__author__ = 'e.kolpakov'


class BaseAgent:
    agent_count_by_type = defaultdict(int)

    def __init__(self, agent_id=None):
        actual_type = type(self)
        self.agent_count_by_type[actual_type] += 1
        self._agent_id = agent_id if agent_id else actual_type.__name__ + str(self.agent_count_by_type[actual_type])
        self._env = None
        self._observers_cache = None
        super(BaseAgent, self).__init__()

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

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "{type} {id}".format(type=type(self).__name__, id=self._agent_id)

    def __lt__(self, other):
        assert type(self) == type(other)
        return self.agent_id < other.agent_id

    def __eq__(self, other):
        assert type(self) == type(other)
        return self.agent_id == other.agent_id

    def __hash__(self):
        return hash(self.agent_id)

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
                observers = get_observers(member)
                for observer in observers:
                    self._observers_cache.append(observer)
        return self._observers_cache

    def __get_member_names(self):
        return [member_name for member_name in dir(self.__class__) if not member_name.startswith('__')]

    def _get_all_callables(self):
        for member_name in self.__get_member_names():
            member = getattr(self, member_name)
            if callable(member):
                yield member

    def _get_all_properties(self):
        for member_name in self.__get_member_names():
            member = getattr(self.__class__, member_name)
            if isinstance(member, property):
                yield member.fget


class IntelligentAgent(BaseAgent):
    pass
