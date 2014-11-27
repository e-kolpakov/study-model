from unittest import mock

import pytest

from agents.resource import Resource
from agents.student.behaviors.resource_choice import RandomResourceChoiceBehavior, RationalResourceChoiceBehavior
from knowledge_representation import Fact, Curriculum
from knowledge_representation.lesson_type import Lecture


__author__ = 'e.kolpakov'


@pytest.fixture
def student():
    return mock.Mock(spec=student)


@pytest.fixture
def curriculum():
    return mock.Mock(spec=Curriculum)


def _make_lecture(code, fact_codes):
    return Lecture(code, (Fact(code) for code in fact_codes))


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

    @pytest.mark.parametrize("lesson1, lesson2, exp_res_id", [
        (['A', 'B', 'C'], ['A', 'B'], 'r1'),
        (['A', 'C'], ['A', 'B', 'C'], 'r2'),
        (['A', 'D'], ['B'], 'r1'),
        (['C'], ['A', 'B'], 'r2'),
    ])
    def test_student_zero_knowledge(self, student, curriculum, behavior, lesson1, lesson2, exp_res_id):
        resources = (
            Resource('r1', [_make_lecture("l1", lesson1)], agent_id='r1'),
            Resource('r2', [_make_lecture("l1", lesson2)], agent_id='r2')
        )

        student.knowledge = set()
        chosen = behavior.choose_resource(student, curriculum, resources)
        assert chosen.name == exp_res_id

    @pytest.mark.parametrize("student_know, lesson1, lesson2, exp_res_id", [
        (['A'], ['A', 'B'], ['A', 'B', 'C'], 'r2'),
        (['A', 'B'], ['A', 'C'], ['B'], 'r1'),
        (['A', 'C'], ['A', 'C'], ['B'], 'r2'),
    ])
    def test_nonzero_student_knowledge(self, student, curriculum, behavior, student_know, lesson1, lesson2, exp_res_id):
        resources = (
            Resource('r1', [_make_lecture("l1", lesson1)], agent_id='r1'),
            Resource('r2', [_make_lecture("l2", lesson2)], agent_id='r2')
        )
        student.knowledge = set([Fact(comp) for comp in student_know])
        chosen = behavior.choose_resource(student, curriculum, resources)
        assert chosen.name == exp_res_id