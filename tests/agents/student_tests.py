import logging
import unittest
from unittest import mock
from unittest.mock import patch

from nose_parameterized import parameterized

import agents
from agents.behaviors.student.behavior_group import BehaviorGroup
from agents.behaviors.student.knowledge_acquisition import BaseKnowledgeAcquisitionBehavior
from agents.behaviors.student.resource_choice import BaseResourceChoiceBehavior
from study_model.competency import Competency
from agents.resource import Resource
from agents.student import Student
from simulation_engine.topics import Topics


__author__ = 'john'


class StudentTests(unittest.TestCase):
    _student = None
    _resource_lookup = None
    _competency_lookup = None
    _behavior_group = None

    def setUp(self):
        self._behavior_group = mock.Mock(BehaviorGroup)
        self._behavior_group.resource_choice = mock.Mock(BaseResourceChoiceBehavior)
        self._behavior_group.knowledge_acquisition = mock.Mock(BaseKnowledgeAcquisitionBehavior)
        self._student = Student("student", {}, self._behavior_group, agent_id='s1')
        """ :type: Student """
        self._competency_lookup = mock.Mock()
        self._resource_lookup = mock.Mock()
        self._competency_lookup.get_competency = mock.Mock(side_effect=self._to_competency)

        self._student.competency_lookup_service = self._competency_lookup
        self._student.resource_lookup_service = self._resource_lookup

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

    def test_get_knowledge_non_zero_competency(self):
        self._student._competencies = {'A': 0, 'B': 0.4, 'C': 0.5}

        result = self._student.get_knowledge(tuple(['A', 'B', 'C']))

        expected = {'A': 0, 'B': 0.4, 'C': 0.5}

        self.assertSequenceEqual(result, expected)

    def test_get_knowledge_given_empty_competencies_list_returns_all_competencies(self):
        self._student._competencies = {'A': 0, 'B': 0.4, 'C': 0.5}

        result = self._student.get_knowledge()

        self.assertSequenceEqual(result, {'A': 0, 'B': 0.4, 'C': 0.5})

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
        resource1 = Resource('A', {'A': 0.5, 'B': 0.2})
        resource2 = Resource('B', {'A': 0.1, 'B': 0.3})
        resources = [resource1, resource2]
        self._resource_lookup.get_accessible_resources = mock.Mock(return_value=resources)
        self._behavior_group.resource_choice.choose_resource = mock.Mock(return_value=resource1)

        with patch.object(self._student, 'study_resource') as patched_study_resource:
            self._student.study()
            self._behavior_group.resource_choice.choose_resource.assert_called_once_with(self._student, resources)
            patched_study_resource.assert_called_once_with(resource1)

    def test_study_resource_updates_student_competencies(self):
        resource1 = Resource('A', {'A': 0.5, 'B': 0.2,  'C': 0.5})
        self._student._competencies = {'A': 0, 'B': 0.4, 'C': 0.5}

        self._behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value=resource1.competencies)

        self._student.study_resource(resource1)

        self.assertAlmostEqual(self._student.competencies['A'], 0.5)
        self.assertAlmostEqual(self._student.competencies['B'], 0.6)
        self.assertAlmostEqual(self._student.competencies['C'], 1.0)

    def test_study_resource_sends_messages(self):
        resource1 = Resource('A', {'A': 0.5, 'B': 0.2,  'C': 0.5, 'D': 0.7})
        self._student._competencies = {'A': 0, 'B': 0.3, 'C': 0.5, 'D': 0.5}
        expected_snapshot = {'A': 0.5, 'B': 0.5, 'C': 1.0, 'D': 1.0}
        expected_delta = {'A': 0.5, 'B': 0.2, 'C': 0.5, 'D': 0.3}

        self._behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value=resource1.competencies)

        with patch('agents.student.pub', spec=True) as pub_mock:
            self._student.study_resource(resource1)

            pub_mock.sendMessage.assert_any_call(
                Topics.RESOURCE_USAGE, student=self._student, resource=resource1)
            # pub_mock.sendMessage.assert_any_call(
            #     Topics.KNOWLEDGE_SNAPSHOT, student=self._student, resource=expected_snapshot)
            # pub_mock.sendMessage.assert_any_call(
            #     Topics.KNOWLEDGE_DELTA, student=self._student, resource=expected_delta)

    def test_get_value_multiplier_returns_knowledge_acquisition_behavior_result(self):
        resource1 = Resource('A', {})

        self._behavior_group.knowledge_acquisition.calculate_prerequisites_multiplier = mock.Mock(return_value=0.8)

        result = self._student.get_value_multiplier(resource1, 'A')

        self.assertEqual(result, 0.8)

        self._behavior_group.knowledge_acquisition.calculate_prerequisites_multiplier.assert_called_once_with(
            self._student, resource1, self._to_competency('A')
        )