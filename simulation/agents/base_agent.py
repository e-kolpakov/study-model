from collections import defaultdict
from simulation.schedulers import scheduled_attr, get_scheduler


class BaseAgent:
    agent_count_by_type = defaultdict(int)

    def __init__(self, agent_id=None):
        actual_type = type(self)
        self.agent_count_by_type[actual_type] += 1
        self._agent_id = agent_id if agent_id else actual_type.__name__ + str(self.agent_count_by_type[actual_type])

    @property
    def agent_id(self):
        return self._agent_id

    def execute_step(self, step_number):
        for method, scheduler in self._get_all_scheduled():
            if scheduler.check_execution_condition(step_number):
                method()

    def _get_all_scheduled(self):
        for member_name in dir(self):
            member = getattr(self, member_name)
            if callable(member):
                scheduler = get_scheduler(member)
                if scheduler:
                    yield member, scheduler


    def __str__(self):
        return "Agent {0}.{1}".format(self.__class__.__name__, self.agent_id)

    def __unicode__(self):
        return u"Agent {0}.{1}".format(self.__class__.__name__, self.agent_id)

    def __repr__(self):
        return self.__str__()