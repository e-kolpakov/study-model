__author__ = 'john'


class Competency:
    def __init__(self, code, facts, dependencies=None):
        """
        :type code: str
        :type dependencies: list[str]
        :type facts: list[Fact]
        """
        self._code = code
        self._facts = frozenset(facts)
        self._dependencies = set(dependencies if dependencies else [])

    @property
    def code(self):
        """
        :rtype: str
        """
        return self._code

    @property
    def dependencies(self):
        """
        :rtype: frozenset[str]
        """
        return self._dependencies

    @property
    def facts(self):
        """
        :rtype: frozenset[Fact]
        """
        return self._facts

    def is_mastered(self, fact_set):
        return set(fact_set) >= self._facts

    def is_available(self, mastered_competencies):
        return set(mastered_competencies) >= self._dependencies

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    def __repr__(self):
        return "{code} <= {dependencies}".format(code=self.code, dependencies=self.dependencies)

    def __eq__(self, other):
        return self.code == other.code

    def __lt__(self, other):
        return self.code in other.dependencies

    def __gt__(self, other):
        return other.code in self.dependencies

    def __hash__(self):
        return hash(self.code)


class ResourceCompetency:
    def __init__(self, competency, enabled_facts=None, disabled_facts=None):
        """
        :param competency: Competency
        :param enabled_facts: list[str] | None
        :param disabled_facts: list[str] | None
        """
        self._competency = competency
        self._enabled_facts = enabled_facts
        self._disabled_facts = disabled_facts

    @property
    def competency(self):
        return self._competency