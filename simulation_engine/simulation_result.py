from collections import defaultdict
from decimal import Decimal

from agents.resource import Resource

__author__ = 'john'


class SimulationResult(object):
    def __init__(self, simulation_step):
        self._simulation_step = simulation_step
        self._resource_usage = defaultdict(int)
        self._competencies_snapshot = dict()
        self._competenices_delta = dict()

    def add_resource_usage(self, resource):
        """
        :type resource: Resource
        """
        self._resource_usage[resource.name] += 1

    def register_knowledge_snapshot(self, student, competencies):
        """
        :type student: Student
        :type competencies: dict[Competency, double]
        """
        self._competencies_snapshot[student.name] = self._prepare_data(competencies)

    def register_knowledge_delta(self, student, competency_delta):
        """
        :type student: Student
        :type competency_delta: dict[Competency, double]
        """
        self._competenices_delta[student.name] = self._prepare_data(competency_delta)

    def _prepare_data(self, competency_data):
        """
        :type competency_data: dict[Competency, double]
        :rtype: dict[Competency, Decimal]
        """
        return {competency: value for competency, value in competency_data.items()}

    @property
    def resource_usage(self):
        return self._resource_usage

    @property
    def competencies_snapshot(self):
        return self._competencies_snapshot

    @property
    def competenices_delta(self):
        return self._competenices_delta