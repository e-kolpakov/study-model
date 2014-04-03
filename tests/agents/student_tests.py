import unittest
from agents.behaviors.student.behavior_group import BehaviorGroup
from agents.behaviors.student.resource_choice import RationalResourceChoiceBehavior
from agents.competency import Competency
from agents.student import Student
from nose_parameterized import parameterized
from unittest import mock

__author__ = 'john'


class StudentTests(unittest.TestCase):
    def setUp(self):
        default_dehavior = BehaviorGroup()
        default_dehavior.resource_choice = RationalResourceChoiceBehavior()
        self._student = Student("student", {}, default_dehavior, agent_id='s1')
        """ :type: Student """
        competency_lookup = mock.Mock()
        competency_lookup.get_competency = mock.Mock(side_effect=self._to_competency)
        self._student.competency_lookup_service = competency_lookup

    def _to_competency(self, code):
        return Competency(code)

    @parameterized.expand([
        ([Competency('A'), Competency('B'), Competency('C')],),
        ([Competency('X')],),
        ([Competency('QWE'), Competency('ASD')],),
    ])
    def test_get_knowledge_no_knowledge_returns_zero_for_all(self, competencies):
        result = self._student.get_knowledge(competencies)

        expected = {item: 0 for item in competencies}

        self.assertSequenceEqual(result, expected)

    @parameterized.expand([
        (['A', 'B', 'C'],),
        ('X',),
        (['QWE', 'ASD'],)
    ])
    def test_get_knowledge_given_codes_looks_up_competencies(self, competencies):
        result = self._student.get_knowledge(competencies)

        expected = {self._to_competency(item): 0 for item in competencies}

        self.assertSequenceEqual(result, expected)

    def test_get_knowledge_non_zero_competency(self):
        comp = self._to_competency
        self._student._competencies = {comp('A'): 0, comp('B'): 0.4, comp('C'): 0.5}

        result = self._student.get_knowledge([comp('A'), comp('B'), comp('C')])

        expected = {comp('A'): 0, comp('B'): 0.4, comp('C'): 0.5}

        self.assertSequenceEqual(result, expected)

