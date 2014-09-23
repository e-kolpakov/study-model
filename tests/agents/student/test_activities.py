import pytest
from unittest import mock
from unittest.mock import patch

from simpy import Environment
from agents.student import Student
from agents.student.activities import IdleStudentActivity

__author__ = 'e.kolpakov'


@pytest.fixture
def env():
    return Environment()


@pytest.fixture
def student(env):
    student_mock = mock.Mock(spec_set=Student)
    student_mock.env = env
    return student_mock


class TestIdleActivity:
    @pytest.fixture
    def activity(self, student):
        return IdleStudentActivity(student)

    @pytest.mark.parametrize("length", [10, 15, 20, 3, 7, 11])
    def test_activate_sends(self, activity, env, length):
        with patch.object(env, 'timeout') as patched_timeout:
            env.process(activity.activate(length))
            env.run()
            patched_timeout.assert_called_once_with(length)
