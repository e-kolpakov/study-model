from unittest import mock
from unittest.mock import PropertyMock

import pytest

from model.agents.resource import Resource
from model.agents.student.goals import StudyCompetenciesGoal, PassExamGoal
from model.knowledge_representation import Competency, Fact
from model.knowledge_representation.lesson_type import Exam, ExamFeedback


__author__ = 'e.kolpakov'

DEFAULT_EXAM_CODE = "EXAM_CODE"


def _make_resource(agent_id, facts, exams):
    result = mock.Mock(spec_set=Resource)
    type(result).agent_id = PropertyMock(return_value=agent_id)
    type(result).facts_to_study = PropertyMock(return_value=facts)
    type(result).exams = PropertyMock(return_value=exams)
    return result


def _make_competency(facts, is_mastered):
    result = mock.Mock(spec_set=Competency)
    type(result).facts = PropertyMock(return_value=facts)
    result.is_mastered = mock.Mock(return_value=is_mastered)
    return result


def _fact_weight(target=0, dependency=0, other=0, cls=StudyCompetenciesGoal):
    result = sum([
        target * cls.TARGET_FACT_WEIGHT,
        dependency * cls.DEPENDENCY_FACT_WEIGHT,
        other * cls.OTHER_FACT_WEIGHT
    ])
    return result


def _make_fact(code, dependencies):
    result = mock.Mock(spec_set=Fact)
    type(result).code = PropertyMock(return_value=code)
    type(result).dependencies = PropertyMock(return_value=dependencies)
    return result


def _make_exam(code, facts):
    result = mock.Mock(spec_set=Exam)
    type(result).code = PropertyMock(return_value=code)
    type(result).facts = PropertyMock(return_value=facts)
    return result


class TestStudyCompetenciesGoal:
    def _get_resource_map(self, student, curriculum, target_facts, res_map):
        target_competency = _make_competency(target_facts, False)
        goal = StudyCompetenciesGoal([target_competency])

        resources = [
            _make_resource(index, [_make_fact(code, []) for code in resource_facts], [])
            for index, resource_facts in res_map.items()
        ]

        with mock.patch('agents.student.goals.get_available_facts') as available_facts_mock:
            available_facts_mock.side_effect = lambda res, stud: res
            resource_map = goal.resource_choice_map(student, curriculum, resources)
            return {resource.agent_id: weight for resource, weight in resource_map.items()}

    @pytest.mark.parametrize("mastered_responses, expected_result", [
        ((False,), False),
        ((True,), True),
        ((True, False), False),
        ((False, False), False),
        ((True, True), True),
    ])
    def test_achieved(self, student, mastered_responses, expected_result):
        competencies = [_make_competency([], mastered) for mastered in mastered_responses]
        goal = StudyCompetenciesGoal(competencies)
        assert goal.achieved(student) == expected_result

    @pytest.mark.parametrize("target_facts, res_map, expected_weights", [
        (['A'], {'r1': ['A']}, {'r1': _fact_weight(target=1)}),
        (['A'], {'r1': ['B']}, {'r1': _fact_weight(other=1)}),
        (['A'], {'r1': ['A', 'B']}, {'r1': _fact_weight(target=1, other=1)}),
        (['A', 'B'], {'r1': ['A', 'B']}, {'r1': _fact_weight(target=2)}),
        (
            ['A', 'B'],
            {'r1': ['A'], 'r2':['B']},
            {'r1': _fact_weight(target=1), 'r2': _fact_weight(target=1)}
        ),
        (
            ['A', 'B', 'C'],
            {'r1': ['A', 'C'], 'r2':['B', 'D'], 'r3': ['A', 'B', 'C', 'D']},
            {'r1': _fact_weight(target=2), 'r2': _fact_weight(target=1, other=1), 'r3': _fact_weight(target=3, other=1)}
        ),
    ])
    def test_resource_choice_map_no_dependencies(self, student, curriculum, target_facts, res_map, expected_weights):
        target_facts = [_make_fact(code, []) for code in target_facts]
        assert self._get_resource_map(student, curriculum, target_facts, res_map) == expected_weights

    @pytest.mark.parametrize("target_facts, res_map, expected_weights", [
        ({'A': ['B']}, {'r1': ['A']}, {'r1': _fact_weight(target=1)}),
        ({'A': ['B']}, {'r1': ['B']}, {'r1': _fact_weight(dependency=1)}),
        ({'A': ['B', 'C']}, {'r1': ['B', 'C']}, {'r1': _fact_weight(dependency=2)}),
        ({'A': ['B'], 'B':[]}, {'r1': ['A', 'B']}, {'r1': _fact_weight(target=2, dependency=1)}),
        ({'A': ['B'], 'B':[]}, {'r1': ['B']}, {'r1': _fact_weight(target=1, dependency=1)}),
        (
            {'A': ['B'], 'B':[]},
            {'r1': ['A'], 'r2': ['A', 'B', 'D'], 'r3':['C', 'D']},
            {
                'r1': _fact_weight(target=1),
                'r2': _fact_weight(target=2, dependency=1, other=1),
                'r3': _fact_weight(other=2),
            }
        ),
    ])
    def test_resource_choice_map(self, student, curriculum, target_facts, res_map, expected_weights):
        target_facts = [_make_fact(code, dependencies) for code, dependencies in target_facts.items()]
        assert self._get_resource_map(student, curriculum, target_facts, res_map) == expected_weights


class TestPassExamGoal:
    @pytest.mark.parametrize("exam_results, expected_result", [
        ({}, False),
        ({DEFAULT_EXAM_CODE: [False]}, False),
        ({DEFAULT_EXAM_CODE: [True]}, True),
        ({DEFAULT_EXAM_CODE: [False, True]}, True),
        ({DEFAULT_EXAM_CODE: [False, False]}, False),
        ({"OTHER": [True]}, False),
        ({"OTHER": [True], DEFAULT_EXAM_CODE:[False]}, False),
        ({"OTHER": [False], DEFAULT_EXAM_CODE:[True]}, True),
    ])
    def test_achieved(self, student, exam_results, expected_result):
        exam = _make_exam(DEFAULT_EXAM_CODE, [])
        type(student).exam_results = PropertyMock(return_value={
            code: [ExamFeedback(exam, 0, feedback, 1) for feedback in feedbacks]
            for code, feedbacks in exam_results.items()
        })
        goal = PassExamGoal(exam)
        assert goal.achieved(student) == expected_result

    @pytest.mark.parametrize("target_facts, reduced_expected_map", [
        (
            {"A": []},
            {
                'r1': _fact_weight(cls=PassExamGoal, target=1),
                'r2': _fact_weight(cls=PassExamGoal, target=1),
                'r3': _fact_weight(cls=PassExamGoal, target=1),
                'r4': _fact_weight(cls=PassExamGoal, target=1),
                'r5': _fact_weight(cls=PassExamGoal, target=1),
                'r6': _fact_weight(cls=PassExamGoal),
            }
        ),
        (
            {"A": [], "B":[]},
            {
                'r1': _fact_weight(cls=PassExamGoal, target=1),
                'r2': _fact_weight(cls=PassExamGoal, target=2),
                'r3': _fact_weight(cls=PassExamGoal, target=2),
                'r4': _fact_weight(cls=PassExamGoal, target=1),
                'r5': _fact_weight(cls=PassExamGoal, target=2),
                'r6': _fact_weight(cls=PassExamGoal, target=1),
            },
        ),
        (
            {"A": ["B"]},
            {
                'r1': _fact_weight(cls=PassExamGoal, target=1),
                'r2': _fact_weight(cls=PassExamGoal, target=1, dependency=1),
                'r3': _fact_weight(cls=PassExamGoal, target=1, dependency=1),
                'r4': _fact_weight(cls=PassExamGoal, target=1),
                'r5': _fact_weight(cls=PassExamGoal, target=1, dependency=1),
                'r6': _fact_weight(cls=PassExamGoal, dependency=1),
            },
        ),
        (
            {"C": ["B"]},
            {
                'r1': _fact_weight(cls=PassExamGoal, target=0),
                'r2': _fact_weight(cls=PassExamGoal, dependency=1),
                'r3': _fact_weight(cls=PassExamGoal, dependency=1),
                'r4': _fact_weight(cls=PassExamGoal, target=1),
                'r5': _fact_weight(cls=PassExamGoal, dependency=1),
                'r6': _fact_weight(cls=PassExamGoal, target=1, dependency=1),
            },
        )
    ])
    def test_resource_choice_map(self, student, curriculum, target_facts, reduced_expected_map):
        target_facts = [_make_fact(code, dependencies) for code, dependencies in target_facts.items()]
        target_exam = _make_exam(DEFAULT_EXAM_CODE, target_facts)
        other_exam = _make_exam("OTHER", target_facts)
        goal = PassExamGoal(target_exam)

        resources = [
            _make_resource('r1', [_make_fact("A", [])], []),
            _make_resource('r2', [_make_fact("A", []), _make_fact("B", [])], []),
            _make_resource('r3', [_make_fact("A", []), _make_fact("B", [])], [other_exam]),
            _make_resource('r4', [_make_fact("A", []), _make_fact("C", [])], [target_exam]),
            _make_resource('r5', [_make_fact("A", []), _make_fact("B", [])], [target_exam]),
            _make_resource('r6', [_make_fact("B", []), _make_fact("C", [])], [target_exam]),
        ]

        expected_weight_map = {resource.agent_id: 0 for resource in resources}
        expected_weight_map.update(reduced_expected_map)

        with mock.patch('agents.student.goals.get_available_facts') as available_facts_mock:
            available_facts_mock.side_effect = lambda res, stud: res
            resource_map = goal.resource_choice_map(student, curriculum, resources)
            assert {resource.agent_id: weight for resource, weight in resource_map.items()} == expected_weight_map