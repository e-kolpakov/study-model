import logging
import unittest
from unittest import mock
from unittest.mock import patch, PropertyMock

import agents
from agents.behaviors.student.behavior_group import BehaviorGroup
from agents.behaviors.student.knowledge_acquisition import BaseFactsAcquisitionBehavior
from agents.behaviors.student.resource_choice import BaseResourceChoiceBehavior
from study_model.competency import Competency
from agents.resource import Resource
from agents.student import Student
from simulation_engine.topics import Topics
from study_model.fact import Fact


__author__ = 'e.kolpakov'


class StudentTests(unittest.TestCase):
    _student = None
    _resource_lookup = None
    _competency_lookup = None
    _behavior_group = None

    def setUp(self):
        self._behavior_group = mock.Mock(BehaviorGroup)
        self._behavior_group.resource_choice = mock.Mock(BaseResourceChoiceBehavior)
        self._behavior_group.knowledge_acquisition = mock.Mock(BaseFactsAcquisitionBehavior)
        self._student = Student("student", [], self._behavior_group, agent_id='s1')
        """ :type: Student """
        self._competency_lookup = mock.Mock()
        self._resource_lookup = mock.Mock()
        self._competency_lookup.get_competency = mock.Mock(side_effect=self._to_competency)

        self._student.competency_lookup_service = self._competency_lookup
        self._student.resource_lookup_service = self._resource_lookup
        self._curriculum_mock = PropertyMock()
        self._student.curriculum = self._curriculum_mock

    def _to_competency(self, code, facts=None):
        eff_facts = facts if facts else []
        return Competency(code, eff_facts)

    def test_study_no_resources_logs_and_returns(self):
        logger = logging.getLogger(agents.student.__name__)
        self._resource_lookup.get_accessible_resources = mock.Mock(return_value=[])
        with patch.object(logger, 'warn') as mocked_warn, \
                patch.object(self._student, '_choose_resource') as resource_choice:
            self._student.study()
            mocked_warn.assert_called_once_with("No resources available")
            self.assertSequenceEqual(resource_choice.call_args_list, [])
            self.assertFalse(resource_choice.called)

    def test_study_uses_behavior_to_choose_and_passes_to_study_resource(self):
        resource1 = Resource('A', [])
        resource2 = Resource('B', [])
        resources = [resource1, resource2]
        self._resource_lookup.get_accessible_resources = mock.Mock(return_value=resources)
        self._behavior_group.resource_choice.choose_resource = mock.Mock(return_value=resource1)

        with patch.object(self._student, 'study_resource') as patched_study_resource:
            self._student.study()
            self._behavior_group.resource_choice.choose_resource.assert_called_once_with(
                self._student, self._curriculum_mock, resources
            )
            patched_study_resource.assert_called_once_with(resource1)

    def test_study_resource_updates_student_competencies(self):
        resource1 = Resource('A', [])
        self._student._knowledge = {Fact('A'), Fact('C')}
        self._behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value={Fact('A'), Fact('B')})

        self._student.study_resource(resource1)

        self.assertEqual(self._student.knowledge, {Fact('A'), Fact('B'), Fact('C')})

    def test_study_resource_sends_messages(self):
        resource1 = Resource('A', [])
        self._student._knowledge = {Fact('A'), Fact('B')}
        self._behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value={Fact('C'), Fact('D')})

        expected_snapshot = {Fact('A'), Fact('B'), Fact('C'), Fact('D')}
        expected_delta = {Fact('C'), Fact('D')}

        with patch('agents.student.pub', spec=True) as pub_mock:
            self._student.study_resource(resource1)

            pub_mock.sendMessage.assert_any_call(
                Topics.RESOURCE_USAGE, student=self._student, resource=resource1)
            pub_mock.sendMessage.assert_any_call(
                Topics.KNOWLEDGE_SNAPSHOT, student=self._student, knowledge=expected_snapshot)
            pub_mock.sendMessage.assert_any_call(
                Topics.KNOWLEDGE_DELTA, student=self._student, knowledge_delta=expected_delta)