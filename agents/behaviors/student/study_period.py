import random

__author__ = 'e.kolpakov'


class BaseStudyPeriodBehavior:
    def get_study_period(self, student, current_time):
        """
        Gets time span for studying resources
        :param student:
        :return: double
        """
        raise NotImplemented()

    def get_idle_period(self, student, current_time):
        """
        Gets time span between study serssions
        :param student:
        :return: double
        """
        raise NotImplemented()


class FixedStudyPeriodBehavior(BaseStudyPeriodBehavior):
    def __init__(self, study_period=10, idle_period=20):
        self._idle_period = idle_period
        self._study_period = study_period

    def get_study_period(self, student, current_time):
        return self._study_period

    def get_idle_period(self, student, current_time):
        return self._idle_period


class RandomStudyPeriodBehavior(BaseStudyPeriodBehavior):
    def __init__(self, max_study_period=10, max_idle_period=20):
        self._max_idle_period = max_idle_period
        self._max_study_period = max_study_period

    def get_study_period(self, student, current_time):
        return round(random.random() * self._max_study_period, 2)

    def get_idle_period(self, student, current_time):
        return round(random.random() * self._max_idle_period, 2)

