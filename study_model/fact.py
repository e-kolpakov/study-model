__author__ = 'john'


class Fact:
    def __init__(self, code, dependencies=None):
        """
        :param code: str
        :param dependencies: list[str] | tuple[str] | None
        """
        self._code = code
        self._dependencies = frozenset(dependencies if dependencies else [])

    @property
    def code(self):
        return self._code

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


class ResourceFact:
    def __init__(self, fact):
        """
        :type fact: Fact
        """
        self._fact = fact

    @property
    def fact(self):
        """
        :rtype: Fact
        """
        return self._fact

    def __str__(self):
        return "ResourceFact [{0}]".format(self.fact.code)

    def __repr__(self):
        return "ResourceFact [{0}] (id: {1})".format(self.fact.code, id(self))

