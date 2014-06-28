__author__ = 'e.kolpakov'


class Competency:
    def __init__(self, code, facts):
        """
        :type code: str
        :type facts: list[Fact]
        """
        self._code = code
        self._facts = frozenset(facts)

    @property
    def code(self):
        """
        :rtype: str
        """
        return self._code

    @property
    def facts(self):
        """
        :rtype: frozenset[Fact]
        """
        return self._facts

    def is_mastered(self, fact_set):
        return set(fact_set) >= self._facts

    def mastered_ratio(self, knowledge):
        """
        Calculates known facts to all facts ratio as number in interval [0, 1]
        :param knowledge: set[Fact] | frozenset[Fact]
        :return: double
        """
        return len(knowledge & self._facts) / len(self._facts)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    def __repr__(self):
        return "{code} <= {facts}".format(code=self.code, facts=self.facts)

    def __eq__(self, other):
        return self.code == other.code

    def __lt__(self, other):
        return self.code in other.dependencies

    def __hash__(self):
        return hash(self.code)