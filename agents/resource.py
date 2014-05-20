from agents.base_agent import BaseAgent

__author__ = 'john'


class Resource(BaseAgent):
    def __init__(self, name, resource_facts, behavior=None, *args, **kwargs):
        """
        :type name: str
        :type resource_facts: list[ResourceFact]
        """
        super(Resource, self).__init__(*args, **kwargs)
        self._name = name
        self._behavior = behavior
        self._facts = resource_facts

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @property
    def facts(self):
        """
        :rtype: tuple[ResourceFact]
        """
        return tuple(self._facts)