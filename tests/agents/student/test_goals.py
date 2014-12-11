from unittest import mock
from unittest.mock import PropertyMock

import pytest

from agents.resource import Resource
from agents.student.goals import StudyCompetenciesGoal
from knowledge_representation import Competency, Fact


__author__ = 'e.kolpakov'


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
    return target * cls.TARGET_FACT_WEIGHT + dependency * cls.DEPENDENCY_FACT_WEIGHT + other * cls.OTHER_FACT_WEIGHT


class TestStudyCompetenciesGoal:
    def _make_fact(self, code, dependencies):
        result = mock.Mock(spec_set=Fact)
        type(result).code = PropertyMock(return_value=code)
        type(result).dependencies = PropertyMock(return_value=dependencies)
        return result

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
        target_facts = [self._make_fact(code, []) for code in target_facts]
        target_competency = _make_competency(target_facts, False)
        goal = StudyCompetenciesGoal([target_competency])

        resources = [
            _make_resource(index, [self._make_fact(code, []) for code in resource_facts], [])
            for index, resource_facts in res_map.items()
        ]

        with mock.patch('agents.student.goals.get_available_facts') as available_facts_mock:
            available_facts_mock.side_effect = lambda res, stud: res
            resource_map = goal.resource_choice_map(student, curriculum, resources)
            result = {resource.agent_id: weight for resource, weight in resource_map.items()}
            assert result == expected_weights

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
        target_facts = [self._make_fact(code, dependencies) for code, dependencies in target_facts.items()]
        target_competency = _make_competency(target_facts, False)
        goal = StudyCompetenciesGoal([target_competency])

        resources = [
            _make_resource(index, [self._make_fact(code, []) for code in resource_facts], [])
            for index, resource_facts in res_map.items()
        ]

        with mock.patch('agents.student.goals.get_available_facts') as available_facts_mock:
            available_facts_mock.side_effect = lambda res, stud: res
            resource_map = goal.resource_choice_map(student, curriculum, resources)
            result = {resource.agent_id: weight for resource, weight in resource_map.items()}
            assert result == expected_weights