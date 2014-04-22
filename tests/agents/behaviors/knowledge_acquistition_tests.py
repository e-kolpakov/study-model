import unittest
from unittest import mock
from agents.behaviors import AllPrerequisitesRequiredKnowledgeAcquisitionBehavior
from agents.competency import Competency
from agents.resource import Resource
from agents.student import Student

__author__ = 'john'


class AllPrerequisitesRequiredKnowledgeAcquisitionBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.behavior = AllPrerequisitesRequiredKnowledgeAcquisitionBehavior()
        self.student = mock.Mock(spec=Student)
        self.resource = mock.Mock(spec=Resource)
        self.competency = mock.Mock(spec=Competency)

        self.competency.dependencies = ('A', 'B', 'C')

    def test_calculate_prerequisites_multiplier_student_have_all_prerequisites(self):
        self.student.get_knowledge = mock.Mock(return_value={'A': 1, 'B': 1, 'C': 1})
        self.resource.competencies = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        multiplier = self.behavior.calculate_prerequisites_multiplier(
            self.student, self.resource, self.competency)

        self.assertEqual(multiplier, 1)

    def test_calculate_prerequisites_multiplier_resource_have_all_prerequisites(self):
        self.student.get_knowledge = mock.Mock(return_value={'A': 0, 'B': 0, 'C': 0})
        self.resource.competencies = {'A': 1, 'B': 1, 'C': 1}
        multiplier = self.behavior.calculate_prerequisites_multiplier(
            self.student, self.resource, self.competency)

        self.assertEqual(multiplier, 1)

    def test_calculate_prerequisites_multiplier_student_and_resource_sum_have_all_prerequisites(self):
        self.student.get_knowledge = mock.Mock(return_value={'A': 0.2, 'B': 1, 'C': 0})
        self.resource.competencies = {'A': 0.8, 'B': 0.2, 'C': 1}
        multiplier = self.behavior.calculate_prerequisites_multiplier(
            self.student, self.resource, self.competency)

        self.assertEqual(multiplier, 1)

    def test_not_all_prerequisites_are_met(self):
        self.student.get_knowledge = mock.Mock(return_value={'A': 0, 'B': 1, 'C': 0})
        self.resource.competencies = {'A': 0.8, 'B': 0.2, 'C': 1}
        multiplier = self.behavior.calculate_prerequisites_multiplier(
            self.student, self.resource, self.competency)

        self.assertEqual(multiplier, 0)