import logging
from unittest import mock
from unittest.mock import patch, PropertyMock

import pytest

import agents
from agents.resource import Resource
from agents.student import Student
from behaviors.student.behavior_group import BehaviorGroup
from behaviors.student.knowledge_acquisition import BaseFactsAcquisitionBehavior
from behaviors.student.resource_choice import BaseResourceChoiceBehavior
from behaviors.student.stop_participation import BaseStopParticipationBehavior
from knowledge_representation import Fact
from tests.utils import iterate_event_generator


__author__ = 'e.kolpakov'


@pytest.fixture
def resource_lookup():
    return mock.Mock()


@pytest.fixture
def behavior_group():
    bhg = mock.Mock(BehaviorGroup)
    bhg.resource_choice = mock.Mock(BaseResourceChoiceBehavior)
    bhg.knowledge_acquisition = mock.Mock(BaseFactsAcquisitionBehavior)
    bhg.stop_participation = mock.Mock(BaseStopParticipationBehavior)
    return bhg


@pytest.fixture
def student(behavior_group, curriculum, resource_lookup):
    """
    :rtype: student
    """
    result = Student("student", [], behavior_group, agent_id='s1')
    result.resource_lookup_service = resource_lookup
    result.curriculum = curriculum
    result.env = mock.Mock()
    return result


@pytest.fixture
def curriculum():
    return PropertyMock()


@pytest.fixture
def resource():
    return mock.Mock(spec=Resource)


class TestStudent:
    def test_study_no_resources_logs_and_returns(self, student, resource_lookup, behavior_group):
        logger = logging.getLogger(agents.student.__name__)
        resource_lookup.get_accessible_resources = mock.Mock(return_value=[])
        behavior_group.stop_participation.stop_participation = mock.Mock(return_value=True)
        with patch.object(logger, 'warn') as mocked_warn, \
                patch.object(student, '_choose_resource') as resource_choice, \
                patch.object(student, 'observe'):
            study_gen = student.study()
            iterate_event_generator(study_gen)
            mocked_warn.assert_called_once_with("No resources available")
            assert resource_choice.call_args_list == []
            assert not resource_choice.called

    def test_study_uses_behavior_to_choose_and_passes_to_study_resource(self, student, behavior_group, resource_lookup,
                                                                        curriculum):
        resource1 = Resource('A', [])
        resource2 = Resource('B', [])
        resources = [resource1, resource2]
        resource_lookup.get_accessible_resources = mock.Mock(return_value=resources)
        behavior_group.resource_choice.choose_resource = mock.Mock(return_value=resource1)
        behavior_group.stop_participation.stop_participation = mock.Mock(return_value=True)

        with patch.object(student, 'study_resource') as patched_study_resource, patch.object(student, 'observe'):
            study_gen = student.study()
            iterate_event_generator(study_gen)
            behavior_group.resource_choice.choose_resource.assert_called_once_with(student, curriculum, resources)
            patched_study_resource.assert_called_once_with(resource1)

    def test_study_resource_updates_student_competencies(self, student, behavior_group):
        resource1 = Resource('A', [])
        student._knowledge = {Fact('A'), Fact('C')}
        behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value={Fact('A'), Fact('B')})

        with patch.object(student, 'observe'):
            student.study()
            student.study_resource(resource1)

        assert student.knowledge == {Fact('A'), Fact('B'), Fact('C')}

    def test_study_resource_triggers_observe(self, student, behavior_group, resource):
        behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value=set())
        with patch.object(student, 'observe') as observe_mock:
            student.study_resource(resource)
            observe_mock.assert_called_once_with()