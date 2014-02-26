from collections import defaultdict

__author__ = 'john'


class BaseAgent(object):
    agent_count_by_type = defaultdict(int)

    def __init__(self, agent_id=None):
        actual_type = type(self)
        self.agent_count_by_type[actual_type] += 1
        self._agent_id = agent_id if agent_id else actual_type.__name__ + self.agent_count_by_type[actual_type]

    @property
    def agent_id(self):
        return self._agent_id

    def act(self):
        raise NotImplemented()
