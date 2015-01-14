from unittest.mock import patch

import pytest

from agents.student.activities import IdleActivity, StudySessionActivity


__author__ = 'e.kolpakov'


class TestIdleActivity:
    @pytest.mark.parametrize("length", [10, 15, 20, 3, 7, 11])
    def test_activate_sends(self, student, env, length):
        activity = IdleActivity(student, length, env)
        # noinspection PyUnresolvedReferences
        with patch.object(env, 'timeout') as patched_timeout:
            env.process(activity.run(length))
            env.run()
            patched_timeout.assert_called_once_with(length)


class TestStudySessionActivity:
    @pytest.fixture
    def activity(self, student):
        return StudySessionActivity(student)