import unittest
from unittest import mock
from nose_parameterized import parameterized
from agents.behaviors import RandomResourceChoiceBehavior, RationalResourceChoiceBehavior
from agents.resource import Resource
from agents.student import Student

__author__ = 'john'


class RandomResourceChoiceBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.student = mock.Mock()
        self.behavior = RandomResourceChoiceBehavior()

    def test_choose_from_given_resources(self):
        resources = (Resource('r1', {}, None), Resource('r2', {}, None))
        chosen = self.behavior.choose_resource(self.student, resources)

        self.assertTrue(chosen in resources)


class RationalResourceChoiceBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.student = mock.Mock(spec=Student)
        self.behavior = RationalResourceChoiceBehavior()

    @parameterized.expand([
        ('complete_superiority_r2', {'a': 0.1, 'b': 0.5}, {'a': 0.2, 'b': 0.6}, 'r2'),
        ('partial_superiority1_r2', {'a': 0.1, 'b': 0.5}, {'a': 0.1, 'b': 0.6}, 'r2'),
        ('partial_superiority2_r2', {'a': 0.1, 'b': 0.5}, {'a': 0.2, 'b': 0.5}, 'r2'),
        ('sum_superiority1_r2', {'a': 0.2, 'b': 0.3}, {'a': 0.1, 'b': 0.5}, 'r2'),
        ('sum_superiority2_r1', {'a': 0.2, 'b': 0.3}, {'a': 0.3, 'b': 0.1}, 'r1'),
        ('different_competencies_r1', {'a': 0.2, 'b': 0.3}, {'c': 0.2, 'b': 0.1}, 'r1'),
    ])
    def test_student_zero_knowledge(self, _, first_competencies, second_competencies, expected_resource_id):
        resources = (
            Resource('r1', first_competencies, None, agent_id='r1'),
            Resource('r2', second_competencies, None, agent_id='r2')
        )

        self.student.competencies = dict()
        self.student.get_value_multiplier = mock.Mock(spec=Student.get_value_multiplier, return_value=1)
        chosen = self.behavior.choose_resource(self.student, resources)
        self.assertEqual(chosen.name, expected_resource_id)

    @parameterized.expand([
        ('a_saturated', {'a': 0.8, 'b': 0.1}, {'a': 0.2, 'b': 0.3}, {'a': 1.0, 'b': 0.0}, 'r2'),
        ('a_started', {'a': 0.8, 'b': 0.1}, {'a': 0.2, 'b': 0.3}, {'a': 0.7, 'b': 0.0}, 'r1'),
    ])
    def test_nonzero_student_knowledge(self, _, comp1, comp2, comp_student, expected_resource_id):
        resources = (
            Resource('r1', comp1, None, agent_id = 'r1'),
            Resource('r2', comp2, None, agent_id = 'r2'),
        )
        self.student.competencies = comp_student
        self.student.get_value_multiplier = mock.Mock(spec=Student.get_value_multiplier, return_value=1)
        chosen = self.behavior.choose_resource(self.student, resources)
        self.assertEqual(chosen.name, expected_resource_id)