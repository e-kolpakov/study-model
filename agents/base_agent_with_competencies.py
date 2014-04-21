from copy import deepcopy
from agents.base_agent import BaseAgent

__author__ = 'john'


class BaseAgentWithCompetencies(BaseAgent):
    def __init__(self, competencies, *args, **kwargs):
        """
        :type competencies: dict[str, double]
        """
        super().__init__(*args, **kwargs)
        self._competencies = deepcopy(competencies)
        """
        :type: dict[str, double]
        """

    @property
    def competencies(self):
        """
        :rtype: dict[str, double]
        """
        return self._competencies
