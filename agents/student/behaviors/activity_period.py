from abc import ABCMeta, abstractmethod
import random

__author__ = 'e.kolpakov'


class BaseActivityLengthsBehavior(metaclass=ABCMeta):
    def __init__(self, idle_period=10, study_period=20, peer_interaction_period=5, pass_exam_period=5):
        self._idle_period = idle_period
        self._study_period = study_period
        self._peer_interaction_period = peer_interaction_period
        self._pass_exam_period = pass_exam_period

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
        Gets time span between study sessions
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
    def get_study_period(self, student, current_time):
        return self._study_period

    def get_idle_period(self, student, current_time):
        return self._idle_period

    def get_peer_interaction_period(self, student, current_time):
        return self._peer_interaction_period

    def get_pass_exam_period(self, student, current_time):
        return self._pass_exam_period


class RandomActivityLengthsBehavior(BaseActivityLengthsBehavior):
    @staticmethod
    def _get_rounded_random(max_value, decimal_points=2):
        return round(random.random() * max_value, decimal_points)

    def get_idle_period(self, student, current_time):
        return self._get_rounded_random(self._idle_period)

    def get_study_period(self, student, current_time):
        return self._get_rounded_random(self._study_period)

    def get_peer_interaction_period(self, student, current_time):
        return self._get_rounded_random(self._peer_interaction_period)

    def get_pass_exam_period(self, student, current_time):
        return self._get_rounded_random(self._pass_exam_period)


class QuarterHourRandomActivityLengthsBehavior(BaseActivityLengthsBehavior):
    @staticmethod
    def _get_random_quarters(max_value):
        return random.randrange(max_value*4) * 1.0 / 4.0

    def get_idle_period(self, student, current_time):
        return self._get_random_quarters(self._idle_period)

    def get_study_period(self, student, current_time):
        return self._get_random_quarters(self._study_period)

    def get_peer_interaction_period(self, student, current_time):
        return self._get_random_quarters(self._peer_interaction_period)

    def get_pass_exam_period(self, student, current_time):
        return self._get_random_quarters(self._pass_exam_period)