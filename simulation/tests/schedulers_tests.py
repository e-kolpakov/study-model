import unittest
from nose_parameterized import parameterized
from simulation.schedulers import StepScheduler

__author__ = 'e.kolpakov'


class StepSchedulerTests(unittest.TestCase):
    @parameterized.expand([
        ("at_start1", 0, 0, True),
        ("at_start2", 1, 1, True),
        ("beyond_start", 0, 1, True),
        ("before_start1", 3, 1, False),
        ("before_start2", 10, 8, False),
        ("before_start3", 6, 3, False)
    ])
    def test_start_schedule(self, _, start, step_number, expected):
        schedule = StepScheduler(start)
        actual = schedule.check_execution_condition(step_number)
        self.assertEqual(actual, expected)

    @parameterized.expand([
        ("never", 0, 0, 0, False),
        ("once_at_start", 0, 1, 0, True),
        ("at_stop", 0, 1, 1, False),
        ("before_start", 2, 2, 1, False),
        ("once", 2, 3, 2, True),
        ("window1", 2, 5, 2, True),
        ("window2", 2, 5, 3, True),
        ("window3", 2, 5, 4, True),
        ("beyond_stop", 2, 5, 7, False),
    ])
    def test_start_stop_schedule(self, _, start, stop, step_number, expected):
        schedule = StepScheduler(start, stop)
        actual = schedule.check_execution_condition(step_number)
        self.assertEqual(actual, expected)

    @parameterized.expand([
        ("once", 0, 1, 1, 0, True),
        ("twice1", 0, 2, 1, 0, True),
        ("twice2", 0, 2, 1, 1, True),
        ("every_other0", 0, 3, 2, 0, True),
        ("every_other1", 0, 3, 2, 1, False),
        ("every_other2", 0, 3, 2, 2, True),
        ("every_other_shifted1", 1, 4, 2, 1, True),
        ("every_other_shifted1", 1, 4, 2, 2, False),
        ("every_other_shifted1", 1, 4, 2, 3, True),
        ("once_in_five0", 0, 10, 5, 0, True),
        ("once_in_five2", 0, 10, 5, 2, False),
        ("once_in_five4", 0, 10, 5, 5, True),
        ("once_in_five10", 0, 11, 5, 10, True)
    ])
    def test_start_stop_step_schedule(self, _, start, stop, step, step_number, expected):
        schedule = StepScheduler(start, stop, step)
        for i in range(0, step_number):
            schedule.check_execution_condition(i)
        actual = schedule.check_execution_condition(step_number)
        self.assertEqual(actual, expected)