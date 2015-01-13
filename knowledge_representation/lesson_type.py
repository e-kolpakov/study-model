from abc import ABCMeta, abstractmethod
from collections import defaultdict
import logging

from lazy import lazy

from infrastructure import INFINITY


__author__ = 'e.kolpakov'


class BaseLesson(metaclass=ABCMeta):
    def __init__(self, code, publish_at=0, name=None, **kwargs):
        self._code = code

        self.name = name
        self.publish_at = publish_at

        self._logger = logging.getLogger(__name__)

        # noinspection PyArgumentList
        super(BaseLesson, self).__init__(**kwargs)

    @property
    def code(self):
        """
        :rtype: str
        """
        return self._code

    def __eq__(self, other):
        """
        :param other: object to compare to
        :return: bool
        """
        return isinstance(other, type(self)) and self.code == other.code

    def __hash__(self):
        return hash((self.code, type(self)))

    @lazy
    def _format_template(self):
        return "{type} {code}" + " ({name})" if self.name else ""

    @lazy
    def _get_format_parameters(self):
        result = {'type': type(self).__name__, 'code': self.code}
        if self.name:
            result['name'] = self.name
        return result

    def __str__(self):
        return self._format_template.format(**self._get_format_parameters)

    def __unicode__(self):
        return self.__str__()

    @abstractmethod
    def take(self, student, until=None):
        pass


class FactBasedLessonMixin:
    def __init__(self, facts=None, **kwargs):
        # noinspection PyArgumentList
        super(FactBasedLessonMixin, self).__init__(**kwargs)
        self._facts = facts if facts else {}

    @property
    def facts(self):
        """
        :rtype: tuple[knowledge_representation.Fact]
        """
        return frozenset(self._facts)

    @property
    def total_complexity(self):
        return sum(fact.complexity for fact in self.facts)

    def __eq__(self, other):
        return super().__eq__(other) and self.facts == other.facts

    def __hash__(self):
        return super(FactBasedLessonMixin, self).__hash__() * 31 + hash(self.facts)


class Lecture(BaseLesson, FactBasedLessonMixin):
    def take(self, student, until=INFINITY):
        """
        Student learns all facts available in lecture
        :param Student student:
        :param float|None until: upper time bound for activity
        :return: True if had enough time to study all the facts, False otherwise
        """
        knowledge_to_acquire = student.behavior.knowledge_acquisition.acquire_facts(student, self)
        for fact in knowledge_to_acquire:
            success = yield from student.study_fact(fact, until)
            if not success:
                return False

        return True


class Exam(BaseLesson, FactBasedLessonMixin):
    def __init__(self, code, allowed_time=INFINITY, weight=1.0, pass_threshold=0.8, *args, **kwargs):
        super(Exam, self).__init__(code, *args, **kwargs)
        self._weight = weight
        self._pass_threshold = pass_threshold
        self._allowed_time = allowed_time

        self._exam_attempts = defaultdict(int)

    @property
    def weight(self):
        return self._weight

    @property
    def pass_threshold(self):
        return self._pass_threshold

    @property
    def allowed_time(self):
        return self._allowed_time

    def take(self, student, until=INFINITY):
        """
        Student checks all facts available in exam
        :param Student student:
        :param float|None until: upper time bound for activity
        :return ExamFeedback: Exam feedback
        """
        attempt_start = student.env.now
        complete_until = attempt_start + self.allowed_time
        stop_attempt_at = min(until, complete_until)
        self._exam_attempts[student] += 1

        knows, total = 0, float(len(self.facts))
        for fact in self.facts:
            knows_fact = yield from student.check_fact(fact, stop_attempt_at)
            if knows_fact:
                knows += 1

        ratio = knows / total
        return ExamFeedback(ratio, ratio >= self.pass_threshold, self._exam_attempts[student])


class ExamFeedback:
    def __init__(self, grade, passed, attempt_number, feedback=None):
        self.grade = grade
        self.passed = passed
        self.attempt_number = attempt_number
        self.feedback = feedback



