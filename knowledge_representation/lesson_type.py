from abc import ABC, abstractmethod

__author__ = 'e.kolpakov'


class BaseLesson(ABC):
    def __init__(self, code, name):
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

    @abstractmethod
    def interact(self, student):
        pass


class Lecture(BaseLesson):
    def __init__(self, code, name, facts):
        """
        :param str code: lesson code
        :param str name:
        :param frozenset facts:
        """
        super(Lecture, self).__init__(code, name)
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





