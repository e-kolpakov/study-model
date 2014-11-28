from abc import ABC, abstractmethod
import random

__author__ = 'e.kolpakov'


class BaseActivityLengthsBehavior(ABC):
    @abstractmethod
    def get_study_period(self, student, current_time):
        """
        Gets time span for studying resources
        :param student:
        :return: double
        """
        raise NotImplemented()

    @abstractmethod
    def get_idle_period(self, student, current_time):
        """
        Gets time span between study serssions
        :param student:
        :return: double
        """
        raise NotImplemented()

    @abstractmethod
    def get_peer_interaction_period(self, student, current_time):
        """
        Gets time span for sending and reading messages
        :param student:
        :param current_time:
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def get_pass_exam_period(self, student, current_time):
        """
        Gets time span for sending and reading messages
        :param student:
        :param current_time:
        :return:
        """
        raise NotImplemented()


class FixedActivityLengthsBehavior(BaseActivityLengthsBehavior):
    def __init__(self, study_period=10, idle_period=20, peer_interaction_period=2, pass_exam_period=5):
        self._idle_period = idle_period
        self._study_period = study_period
        self._peer_interaction_period = peer_interaction_period
        self._pass_exam_period = pass_exam_period

    def get_study_period(self, student, current_time):
        return self._study_period

    def get_idle_period(self, student, current_time):
        return self._idle_period

    def get_peer_interaction_period(self, student, current_time):
        return self._peer_interaction_period

    def get_pass_exam_period(self, student, current_time):
        return self._pass_exam_period


class RandomActivityLengthsBehavior(BaseActivityLengthsBehavior):
    def __init__(self, max_study_period=10, max_idle_period=20, peer_interaction_period=5, pass_exam_period=5):
        self._max_idle_period = max_idle_period
        self._max_study_period = max_study_period
        self._peer_interaction_period = peer_interaction_period
        self._pass_exam_period = pass_exam_period

    @staticmethod
    def _get_rounded_random(max_value, decimal_points=2):
        return round(random.random() * max_value, decimal_points)

    def get_study_period(self, student, current_time):
        return self._get_rounded_random(self._max_study_period)

    def get_idle_period(self, student, current_time):
        return self._get_rounded_random(self._max_idle_period)

    def get_peer_interaction_period(self, student, current_time):
        return self._get_rounded_random(self._peer_interaction_period)

    def get_pass_exam_period(self, student, current_time):
        return self._get_rounded_random(self._pass_exam_period)


class QuarterHourRandomActivityLengthsBehavior(BaseActivityLengthsBehavior):
    def __init__(self, max_study_period=10, max_idle_period=20, peer_interaction_period=5, pass_exam_period=5):
        self._max_idle_period = max_idle_period
        self._max_study_period = max_study_period
        self._peer_interaction_period = peer_interaction_period
        self._pass_exam_period = pass_exam_period

    @staticmethod
    def _get_random_quarters(max_value):
        return random.randrange(max_value*4) * 1.0 / 4.0

    def get_study_period(self, student, current_time):
        return self._get_random_quarters(self._max_study_period)

    def get_idle_period(self, student, current_time):
        return self._get_random_quarters(self._max_idle_period)

    def get_peer_interaction_period(self, student, current_time):
        return self._get_random_quarters(self._peer_interaction_period)

    def get_pass_exam_period(self, student, current_time):
        return self._get_random_quarters(self._pass_exam_period)