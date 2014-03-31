from copy import deepcopy
from agents.base_agent import BaseAgent

__author__ = 'john'


class BaseAgentWithCompetencies(BaseAgent):
    def __init__(self, competencies, *args, **kwargs):
        """
        :type competencies: dict[Competency, double]
        """
        super().__init__(*args, **kwargs)
        self._competencies = deepcopy(competencies)
        """
        :type: dict[Competency, double]
        """

    @property
    def competencies(self):
        """
        :rtype: dict[Competency, double]
        """
        return self._competencies
