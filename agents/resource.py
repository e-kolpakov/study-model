from agents.base_agent import BaseAgent

__author__ = 'john'


class Resource(BaseAgent):
    def __init__(self, name, resource_competencies, behavior=None):
        """
        :type name: str
        :type resource_competencies: list[ResourceCompetency]
        """
        super(Resource, self).__init__()
        self._name = name
        self._behavior = behavior
        self._competencies = resource_competencies

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @property
    def facts(self):
        """
        :rtype: list[ResourceFact]
        """
        return self._facts