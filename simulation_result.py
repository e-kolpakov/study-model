from collections import defaultdict

from agents.resource import Resource

__author__ = 'john'


class SimulationResult(object):
    def __init__(self, simulation_step):
        self._simulation_step = simulation_step
        self._resource_usage = defaultdict(int)
        self._knowledge_snapshot = dict()
        self._knowledge_delta = dict()

    def add_resource_usage(self, resource):
        """
        :type resource: Resource
        """
        self._resource_usage[resource.name] += 1

    def register_knowledge_snapshot(self, student, knowledge):
        """
        :type student: Student
        :type knowledge: dict[Competency, double]
        """
        self._knowledge_snapshot[student.name] = knowledge

    def register_knowledge_delta(self, student, knowledge_delta):
        """
        :type student: Student
        :type knowledge: dict[Competency, double]
        """
        self._knowledge_delta[student.name] = knowledge_delta

    @property
    def resource_usage(self):
        return self._resource_usage

    @property
    def knowledge_snapshot(self):
        return self._knowledge_snapshot

    @property
    def knowledge_delta(self):
        return self._knowledge_delta