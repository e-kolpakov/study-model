from abc import ABC, abstractmethod

from lazy import lazy


__author__ = 'e.kolpakov'


class BaseLesson(ABC):
    def __init__(self, code, name=None):
        self._code = code

        # name is just a displayed name for the lesson - it's not used in equality checks and hashing,
        # hence it can be mutable
        self.name = name

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
    def interact(self, student):
        pass


class Lecture(BaseLesson):
    def __init__(self, code, facts, **kwargs):
        """
        :param str code: lesson code
        :param str name:
        :param frozenset facts:
        """
        super(Lecture, self).__init__(code, **kwargs)
        self._facts = facts

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
        return super(Lecture, self).__hash__() * 31 + hash(self.facts)

    def interact(self, student):
        super().interact(student)





