from agents.base_agent_with_competencies import BaseAgentWithCompetencies

__author__ = 'john'


class Resource(BaseAgentWithCompetencies):
    def __init__(self, name, competencies, behavior=None, *args, **kwargs):
        """
        :type name: str
        :type competencies: dict[str, double]
        """
        super().__init__(competencies, *args, **kwargs)
        self._name = name
        self._behavior = behavior

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name