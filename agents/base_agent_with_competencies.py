from copy import deepcopy
from agents.base_agent import BaseAgent

__author__ = 'john'


class BaseAgentWithCompetencies(BaseAgent):
    def __init__(self, competencies, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._competencies = deepcopy(competencies)

    @property
    def competencies(self):
        return self._competencies
