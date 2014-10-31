from agents.base_agents import BaseAgent
from simulation.resource_lookup_service import ResourceAccessService

__author__ = 'e.kolpakov'


class Resource(BaseAgent):
    def __init__(self, name, resource_facts, behavior=None, *args, **kwargs):
        """
        :type name: str
        :type resource_facts: list[knowledge_representation.ResourceFact]
        """
        super(Resource, self).__init__(*args, **kwargs)
        self._name = name
        self._behavior = behavior
        self._facts = resource_facts

        self._resource_access_service = None

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @property
    def facts(self):
        """
        :rtype: tuple[knowledge_representation.ResourceFact]
        """
        return tuple(self._facts)

    @property
    def resource_access_service(self):
        """ :rtype: ResourceAccessService """
        return self._resource_access_service

    @resource_access_service.setter
    def resource_access_service(self, value):
        """
        :param value: ResourceAccessService
        """
        if not isinstance(value, ResourceAccessService):
            raise ValueError("expected ResourceAccessService instance, {0} given".format(value))
        self._resource_access_service = value

    def allow_access(self, student):
        return self.resource_access_service.check_access(student, self)
