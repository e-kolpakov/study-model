from unittest import mock
from unittest.mock import patch, PropertyMock

import pytest

from agents.resource import Resource
from agents.student import Student
from knowledge_representation import Fact
from knowledge_representation.lesson_type import Lecture
from simulation.result import ResultTopics


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


# TODO: this class changes too often - add tests when it's stabilized
class TestStudent:
    def test_study_resource_updates_student_competencies(self, student, behavior_group, env):
        resource1 = Resource('A', [Lecture('L1', [Fact('A'), Fact('B')])])
        student._knowledge = {Fact('A'), Fact('C')}
        behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value={Fact('A'), Fact('B')})

        # noinspection PyUnresolvedReferences
        with patch.object(student, 'observe'):
            student.start()
            env.process(student.study_resource(resource1))
            env.run()

        assert student.knowledge == {Fact('A'), Fact('B'), Fact('C')}

    def test_study_resource_triggers_observe(self, student, behavior_group, resource):
        behavior_group.knowledge_acquisition.acquire_facts = mock.Mock(return_value=set())
        with patch('infrastructure.observers.pub.sendMessage') as observe_mock:
            student.study_resource(resource)
            call_args = observe_mock.call_args
            args, kwargs = call_args
            assert args == (ResultTopics.RESOURCE_USAGE, )
            assert kwargs['args'] == (resource, )
            assert kwargs['agent'] == student
