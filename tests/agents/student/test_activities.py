import pytest
from unittest import mock
from unittest.mock import patch, PropertyMock

from agents.student import Student
from agents.student.activities import IdleActivity, StudySessionActivity

__author__ = 'e.kolpakov'

@pytest.fixture
def student(behavior_group, resource_lookup, env):
    student_mock = mock.Mock(spec_set=Student)
    student_mock.behavior = PropertyMock(return_value=behavior_group)
    student_mock.env = env
    student_mock.resource_lookup_service = resource_lookup
    student_mock.curriculum = PropertyMock()
    student_mock.env = env
    return student_mock


class TestIdleActivity:
    @pytest.fixture
    def activity(self, student):
        return IdleActivity(student)

    @pytest.mark.parametrize("length", [10, 15, 20, 3, 7, 11])
    def test_activate_sends(self, activity, env, length):
        with patch.object(env, 'timeout') as patched_timeout:
            env.process(activity.activate(length))
            env.run()
            patched_timeout.assert_called_once_with(length)


class TestStudySessionActibity:
    @pytest.fixture
    def activity(self, student):
        return StudySessionActivity(student)