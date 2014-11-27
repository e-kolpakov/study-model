from abc import ABC, abstractmethod
import logging

from lazy import lazy

from infrastructure import INFINITY


__author__ = 'e.kolpakov'


class BaseLesson(ABC):
    def __init__(self, code, name=None, **kwargs):
        self._code = code

        # name is just a displayed name for the lesson - it's not used in equality checks and hashing,
        # hence it can be mutable
        self.name = name

        self._logger = logging.getLogger(__name__)

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
    def __init__(self, code, pass_threshold=1.0, *args, **kwargs):
        super(Exam, self).__init__(code, *args, **kwargs)
        self._pass_threshold = pass_threshold

    @property
    def pass_threshold(self):
        return self._pass_threshold

    def take(self, student, until=INFINITY):
        """
        Student checks all facts available in exam
        :param Student student:
        :param float|None until: upper time bound for activity
        :return: True if had enough time to check all the facts and knows them all, False otherwise
        """
        for fact in self.facts:
            knows_fact = yield from student.check_fact(fact, until)
            if not knows_fact:
                return False

        return True



