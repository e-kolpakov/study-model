import logging
from unittest import mock
from unittest.mock import patch, PropertyMock

import pytest
from simpy import Environment
from agents.student.activities import StudySessionActivity, IdleActivity
from agents.student.behaviors.study_period import BaseActivityLengthsBehavior
from agents.resource import Resource
from agents.student import Student
from agents.student.behaviors.behavior_group import BehaviorGroup
from agents.student.behaviors.knowledge_acquisition import BaseFactsAcquisitionBehavior
from agents.student.behaviors.resource_choice import BaseResourceChoiceBehavior
from agents.student.behaviors.stop_participation import BaseStopParticipationBehavior
from knowledge_representation import Fact
from simulation.resource_lookup_service import ResourceAccessService


__author__ = 'e.kolpakov'

@pytest.fixture
def student(behavior_group, curriculum, resource_lookup, env):
    """
    :rtype: student
    """
    result = Student("student", [], behavior_group, agent_id='s1')
    result.resource_lookup_service = resource_lookup
    result.curriculum = curriculum
    result.env = env
    return result


@pytest.fixture
def curriculum():
    return PropertyMock()


class TestStudent:
    # def test_study_given_already_stopped_returns_immediately(self, student):
    #     student._stop_participation_event = mock.Mock()
    #     student._stop_participation_event.processed = mock.PropertyMock(return_value=True)
    #     with patch.object(student, 'study_session_activity', spec=StudySessionActivity) as patched_study_session,\
    #         patch.object(student, 'idle_activity', spec=IdleActivity) as patched_idle:
    #         patched_study_session.run = mock.Mock()
    #         patched_idle.run = mock.Mock()
    #         student.study()
    #         assert not patched_study_session.run.called
    #         assert not patched_idle.run.called

    # def test_study_no_resources_logs_and_returns(self, student, resource_lookup, behavior_group, env):
    #     logger = logging.getLogger(agents.student.__name__)
    #     resource_lookup.get_accessible_resources = mock.Mock(return_value=[])
    #     behavior_group.stop_participation.stop_participation = mock.Mock(return_value=True)
    #     behavior_group.activity_periods.get_study_period = mock.Mock(return_value=10)
    #     behavior_group.activity_periods.get_idle_period = mock.Mock(return_value=10)
    #     with patch.object(logger, 'warn') as mocked_warn, \
    #             patch.object(student, '_choose_resource') as resource_choice, \
    #             patch.object(student, 'observe'):
    #         env.process(student.study())
    #         env.run()
    #         mocked_warn.assert_called_once_with("No resources available")
    #         assert resource_choice.call_args_list == []
    #         assert not resource_choice.called

    # def test_study_uses_behavior_to_choose_and_passes_to_study_resource(self, student, behavior_group, resource_lookup,
    #                                                                     curriculum, env):
    #     resource1 = Resource('A', [])
    #     resource2 = Resource('B', [])
    #     resources = [resource1, resource2]
    #     resource_lookup.get_accessible_resources = mock.Mock(return_value=resources)
    #     behavior_group.resource_choice.choose_resource = mock.Mock(return_value=resource1)
    #     behavior_group.stop_participation.stop_participation = mock.Mock(return_value=True)
    #     behavior_group.activity_periods.get_study_period = mock.Mock(return_value=10)
    #     behavior_group.activity_periods.get_idle_period = mock.Mock(return_value=10)
    #
    #     with patch.object(student, 'study_resource') as patched_study_resource, patch.object(student, 'observe'):
    #         patched_study_resource.return_value = (env.timeout(i) for i in range(1))
    #         env.process(student.study())
    #         env.run()
    #         behavior_group.resource_choice.choose_resource.assert_called_once_with(student, curriculum, resources)
    #         patched_study_resource.assert_called_once_with(resource1)

    def test_study_resource_updates_student_competencies(self, student, behavior_group, env):
        resource1 = Resource('A', [])
        student._knowledge = {Fact('A'), Fact('C')}
        behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value={Fact('A'), Fact('B')})

        with patch.object(student, 'observe'):
            student.study()
            env.process(student.study_resource(resource1))
            env.run()

        assert student.knowledge == {Fact('A'), Fact('B'), Fact('C')}

    def test_study_resource_triggers_observe(self, student, behavior_group, resource):
        behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value=set())
        with patch.object(student, 'observe') as observe_mock:
            student.study_resource(resource)
            observe_mock.assert_called_once_with()

    @pytest.mark.parametrize("skill, facts", [
        (1, [Fact("A", complexity=1)]),
        (2, [Fact("A", complexity=1)]),
        (1, [Fact("A", complexity=1), Fact('B', complexity=2)]),
        (6, [Fact("A", complexity=1), Fact('B', complexity=2)]),
    ])
    def test_study_resource_yields_timeout_for_duration_of_study(self, student, behavior_group, resource, env, skill, facts):
        behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value=facts)
        student._skill = skill
        expected_timeouts = [fact.complexity / skill for fact in facts]

        timeout_catcher = []
        old_timeout = env.timeout

        def env_timeout_override(t):
            timeout_catcher.append(t)
            return old_timeout(t)
        with patch.object(env, 'timeout', env_timeout_override):
            env.process(student.study_resource(resource))
            env.run()
        assert timeout_catcher == expected_timeouts

    # def test_study_cycle(self, student, behavior_group, env, resource_lookup):
    #     resources = [Resource('A', []),  Resource('B', [])]
    #     resource_lookup.get_accessible_resources = mock.Mock(return_value=resources)
    #     behavior_group.activity_periods.get_study_period = mock.Mock(return_value=10)
    #     behavior_group.activity_periods.get_idle_period = mock.Mock(return_value=10)
    #     with patch.object(student, '_study_session') as patched_study_session, \
    #         patch.object(student, '_idle_session') as patched_idle_session:
    #         patched_study_session.return_value = (env.timeout(i) for i in [10])
    #         patched_idle_session.return_value = (env.timeout(i) for i in [10])
    #         env.process(student.study())
    #         env.run(until=20)
    #         patched_study_session.assert_called_once_with(10, resources)
    #         patched_idle_session.assert_called_once_with(10)