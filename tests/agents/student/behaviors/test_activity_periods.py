import pytest

from agents.student.behaviors.activity_period import FixedActivityLengthsBehavior, BaseActivityLengthsBehavior, \
    RandomActivityLengthsBehavior, QuarterHourRandomActivityLengthsBehavior


__author__ = 'e.kolpakov'


period_configs = [
    {'study_period': 10, 'idle_period': 20, 'peer_interaction_period': 2, 'pass_exam_period': 5},
    {'study_period': 12, 'idle_period': 15, 'peer_interaction_period': 7, 'pass_exam_period': 3},
]


class BaseActivityLengthBehaviorTest:
    behavior_to_test = BaseActivityLengthsBehavior

    default_times = 5

    def extra_check(self, times):
        return True

    def get_behavior(self, study_period=10, idle_period=20, peer_interaction_period=2, pass_exam_period=5):
        return self.behavior_to_test(
            study_period=study_period, idle_period=idle_period,
            peer_interaction_period=peer_interaction_period, pass_exam_period=pass_exam_period
        )

    def check_periods(self, callback, min_bound=0, max_bound=10, times=None):

        times = [callback() for i in range(times)]
        try:
            assert all(min_bound <= time <= max_bound for time in times)
            assert self.extra_check(times)
        except AssertionError:
            print(times)
            raise

    def verify_all_methods(self, student, parameters, times=None):
        times = times if times else self.default_times
        behavior = self.behavior_to_test(**parameters)
        self.check_periods(
            lambda: behavior.get_study_period(student, 0),
            times=times,
            max_bound=parameters.get('study_period', 10)
        )
        self.check_periods(
            lambda: behavior.get_idle_period(student, 0),
            times=times,
            max_bound=parameters.get('idle_period', 20)
        )
        self.check_periods(
            lambda: behavior.get_peer_interaction_period(student, 0),
            times=times,
            max_bound=parameters.get('peer_interaction_period', 2)
        )
        self.check_periods(
            lambda: behavior.get_pass_exam_period(student, 0),
            times=times,
            max_bound=parameters.get('pass_exam_period', 5)
        )


class RandomizedBehaviorTextMixin:
    default_times = 20
    min_unique_values = 4

    def extra_check(self, times):
        return len(set(times)) >= self.min_unique_values


class TestFixedActivityLengthsBehavior(BaseActivityLengthBehaviorTest):
    behavior_to_test = FixedActivityLengthsBehavior

    def extra_check(self, times):
        return len(set(times)) == 1

    @pytest.mark.parametrize('parameters', period_configs)
    def test_periods(self, student, parameters):
        self.verify_all_methods(student, parameters)


class TestRandomActivityLengthsBehavior(RandomizedBehaviorTextMixin, BaseActivityLengthBehaviorTest):
    behavior_to_test = RandomActivityLengthsBehavior

    @pytest.mark.parametrize('parameters', period_configs)
    def test_periods(self, student, parameters):
        self.verify_all_methods(student, parameters)


class TestQuarterHourRandomActivityLengthsBehavior(RandomizedBehaviorTextMixin, BaseActivityLengthBehaviorTest):
    behavior_to_test = QuarterHourRandomActivityLengthsBehavior

    def extra_check(self, times):
        return len(set(times)) >= self.min_unique_values and all(float(time * 4).is_integer() for time in times)

    @pytest.mark.parametrize('parameters', period_configs)
    def test_periods(self, student, parameters):
        self.verify_all_methods(student, parameters)