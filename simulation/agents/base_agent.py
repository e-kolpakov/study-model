from collections import defaultdict
from simulation.observers import get_observer

from simulation.schedulers import get_scheduler


class BaseAgent:
    agent_count_by_type = defaultdict(int)

    def __init__(self, agent_id=None):
        actual_type = type(self)
        self.agent_count_by_type[actual_type] += 1
        self._agent_id = agent_id if agent_id else actual_type.__name__ + str(self.agent_count_by_type[actual_type])
        self.__scheduled = None
        self.__observables = None

    @property
    def agent_id(self):
        return self._agent_id

    def _scheduled(self):
        if self.__scheduled is None:
            self.__scheduled = list(self._get_all_scheduled())
        return self.__scheduled

    def _observers(self):
        if self.__observables is None:
            self.__observables = list(self._get_all_observables())
        return self.__observables

    def execute_step(self, step_number):
        for method, scheduler in self._scheduled():
            if scheduler.check_execution_condition(step_number):
                method()

        for observer in self._observers():
            observer.observe(step_number)

    def _get_all_scheduled(self):
        for member in self._get_all_callables():
            scheduler = get_scheduler(member)
            if scheduler:
                yield member, scheduler

    def _get_all_observables(self):
        """
        :rtype: list[BaseObserver]
        """
        for member in self._get_all_callables():
            observer = get_observer(member)
            if observer:
                yield observer

    def _get_all_callables(self):
        for member_name in dir(self):
            member = getattr(self, member_name)
            if callable(member) and member.__name__ != '_get_all_callables':
                yield member

    def __str__(self):
        return "Agent {0}.{1}".format(self.__class__.__name__, self.agent_id)

    def __unicode__(self):
        return u"Agent {0}.{1}".format(self.__class__.__name__, self.agent_id)

    def __repr__(self):
        return self.__str__()