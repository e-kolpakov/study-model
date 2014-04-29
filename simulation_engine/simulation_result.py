from collections import defaultdict

from agents.resource import Resource

__author__ = 'john'


class SimulationResult(object):
    def __init__(self, simulation_step):
        self._simulation_step = simulation_step
        self._resource_usage = defaultdict(int)
        self._knowledge = dict()
        self._new_knowledge = dict()

    def add_resource_usage(self, resource):
        """
        :type resource: Resource
        """
        self._resource_usage[resource.name] += 1

    def register_knowledge_snapshot(self, student, knowledge):
        """
        :type student: Student
        :type knowledge: set[Fact]
        """
        self._knowledge[student.name] = knowledge

    def register_knowledge_delta(self, student, new_knowledge):
        """
        :type student: Student
        :type new_knowledge: set[Fact]
        """
        self._new_knowledge[student.name] = new_knowledge

    @property
    def resource_usage(self):
        return self._resource_usage

    @property
    def knowledge(self):
        return self._knowledge

    @property
    def new_knowledge(self):
        return self._new_knowledge