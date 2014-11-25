__author__ = 'e.kolpakov'


class Fact:
    def __init__(self, code, dependencies=None, complexity=1.0):
        """
        :param code: str
        :param dependencies: list[str] | tuple[str] | None
        """
        self._code = code
        self._complexity = complexity
        self._dependencies = frozenset(dependencies if dependencies else [])

    @property
    def code(self):
        """ :return: str """
        return self._code

    @property
    def complexity(self):
        """ :return: double """
        return self._complexity

    @property
    def dependencies(self):
        return self._dependencies

    def is_available(self, known_facts):
        """
        :type known_facts: frozenset[Fact]
        """
        return set(fact.code for fact in known_facts) >= self._dependencies

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return isinstance(other, Fact) and self.code == other.code

    def __str__(self):
        return "Fact [{0}]".format(self.code)

    def __repr__(self):
        return "Fact [{0}] (id: {1}), dependencies:[{2}]".format(self.code, id(self), self.dependencies)


class Competency:
    def __init__(self, code, facts):
        """
        :type code: str
        :type facts: list[knowledge_representation.fact.Fact]
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
        :rtype: frozenset[knowledge_representation.fact.Fact]
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