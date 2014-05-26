import unittest
from unittest import mock

from nose_parameterized import parameterized
from study_model.agents.resource import Resource
from study_model.agents.student import Student

from study_model.behaviors.student.resource_choice import RandomResourceChoiceBehavior, RationalResourceChoiceBehavior
from study_model.knowledge_representation import ResourceFact, Curriculum, Fact


__author__ = 'e.kolpakov'


class RandomResourceChoiceBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.student = mock.Mock()
        self.curriculum = mock.Mock(spec=Curriculum)
        self.behavior = RandomResourceChoiceBehavior()

    def test_choose_from_given_resources(self):
        resources = (Resource('r1', [], None), Resource('r2', [], None))
        chosen = self.behavior.choose_resource(self.student, self.curriculum, resources)

        self.assertTrue(chosen in resources)


class RationalResourceChoiceBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.student = mock.Mock(spec=Student)
        self.curriculum = mock.Mock(spec=Curriculum)
        self.behavior = RationalResourceChoiceBehavior()

    @parameterized.expand([
        ('superset_r1', ['A', 'B', 'C'], ['A', 'B'], 'r1'),
        ('superset_r2', ['A', 'C'], ['A', 'B', 'C'], 'r2'),
        ('no_intersection_r1', ['A', 'D'], ['B'], 'r1'),
        ('no_intersection_r2', ['C'], ['A', 'B'], 'r2'),
    ])
    def test_student_zero_knowledge(self, _, comp1, comp2, expected_resource_id):
        resources = (
            Resource('r1', [ResourceFact(Fact(comp)) for comp in comp1], None, agent_id='r1'),
            Resource('r2', [ResourceFact(Fact(comp)) for comp in comp2], None, agent_id='r2')
        )

        self.student.knowledge = set()
        chosen = self.behavior.choose_resource(self.student, self.curriculum, resources)
        self.assertEqual(chosen.name, expected_resource_id)

    @parameterized.expand([
        ('knows_a', ['A'], ['A', 'B'], ['A', 'B', 'C'], 'r2'),
        ('knows_a_and_b', ['A', 'B'], ['A', 'C'], ['B'], 'r1'),
        ('knows_a_and_c', ['A', 'C'], ['A', 'C'], ['B'], 'r2'),
    ])
    def test_nonzero_student_knowledge(self, _, comp_student, comp1, comp2, expected_resource_id):
        resources = (
            Resource('r1', [ResourceFact(Fact(comp)) for comp in comp1], None, agent_id='r1'),
            Resource('r2', [ResourceFact(Fact(comp)) for comp in comp2], None, agent_id='r2'),
        )
        self.student.knowledge = set([Fact(comp) for comp in comp_student])
        chosen = self.behavior.choose_resource(self.student, self.curriculum, resources)
        self.assertEqual(chosen.name, expected_resource_id)