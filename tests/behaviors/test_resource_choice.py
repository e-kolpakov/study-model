from unittest import mock

import pytest

from agents.resource import Resource
from agents.student.behaviors.resource_choice import RandomResourceChoiceBehavior, RationalResourceChoiceBehavior
from knowledge_representation import Fact, ResourceFact, Curriculum


__author__ = 'e.kolpakov'


@pytest.fixture
def student():
    return mock.Mock(spec=student)


@pytest.fixture
def curriculum():
    return mock.Mock(spec=Curriculum)


class TestRandomResourceChoiceBehavior:
    @pytest.fixture
    def behavior(self):
        return RandomResourceChoiceBehavior()

    def test_choose_from_given_resources(self, student, curriculum, behavior):
        resources = (Resource('r1', [], None), Resource('r2', [], None))
        chosen = behavior.choose_resource(student, curriculum, resources)

        assert chosen in resources


class TestRationalResourceChoiceBehavior:
    @pytest.fixture
    def behavior(self):
        return RationalResourceChoiceBehavior()

    @pytest.mark.parametrize("comp1, comp2, exp_res_id", [
        (['A', 'B', 'C'], ['A', 'B'], 'r1'),
        (['A', 'C'], ['A', 'B', 'C'], 'r2'),
        (['A', 'D'], ['B'], 'r1'),
        (['C'], ['A', 'B'], 'r2'),
    ])
    def test_student_zero_knowledge(self, student, curriculum, behavior, comp1, comp2, exp_res_id):
        resources = (
            Resource('r1', [ResourceFact(Fact(comp)) for comp in comp1], None, agent_id='r1'),
            Resource('r2', [ResourceFact(Fact(comp)) for comp in comp2], None, agent_id='r2')
        )

        student.knowledge = set()
        chosen = behavior.choose_resource(student, curriculum, resources)
        assert chosen.name == exp_res_id

    @pytest.mark.parametrize("student_know, comp1, comp2, exp_res_id", [
        (['A'], ['A', 'B'], ['A', 'B', 'C'], 'r2'),
        (['A', 'B'], ['A', 'C'], ['B'], 'r1'),
        (['A', 'C'], ['A', 'C'], ['B'], 'r2'),
    ])
    def test_nonzero_student_knowledge(self, student, curriculum, behavior, student_know, comp1, comp2, exp_res_id):
        resources = (
            Resource('r1', [ResourceFact(Fact(comp)) for comp in comp1], None, agent_id='r1'),
            Resource('r2', [ResourceFact(Fact(comp)) for comp in comp2], None, agent_id='r2'),
        )
        student.knowledge = set([Fact(comp) for comp in student_know])
        chosen = behavior.choose_resource(student, curriculum, resources)
        assert chosen.name == exp_res_id