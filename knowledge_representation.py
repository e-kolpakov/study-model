from copy import deepcopy
import logging

__author__ = 'e.kolpakov'


def get_available_facts(facts, known_facts):
    """
    :param facts: set[Fact]
    :param known_facts: frozenset[Fact]
    :rtype: frozenset[Fact]
    """
    # TODO: this resembles connected-component search.
    # Might be a good idea to rewrite using connected-component algorithm
    to_check, new_available = deepcopy(facts), deepcopy(known_facts)

    available = deepcopy(known_facts)

    first_iteration = True
    while new_available or first_iteration:
        first_iteration = False
        available |= new_available
        to_check -= new_available
        new_available = set(fact for fact in to_check if fact.is_available(available))

    return frozenset(available & facts - known_facts)


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


class ResourceFact:
    def __init__(self, fact):
        """
        :type fact: knowledge_representation.Fact
        """
        self._fact = fact

    @property
    def fact(self):
        """
        :rtype: knowledge_representation.Fact
        """
        return self._fact

    def __str__(self):
        return "ResourceFact [{0}]".format(self.fact.code)

    def __repr__(self):
        return "ResourceFact [{0}] (id: {1})".format(self.fact.code, id(self))


class Curriculum:
    def __init__(self):
        self._competency_index = {}
        self._fact_index = {}
        self._logger = logging.getLogger(__name__)

    def register_competency(self, competency):
        """
        Registers competency with curriculum.
        :param competency: Competency
        """
        if competency.code in self._competency_index:
            message = "Competency {0} already registered".format(competency)
            self._logger.warn(message)
            raise ValueError(message)

        self._competency_index[competency.code] = competency

    def register_fact(self, fact):
        """
        Registers fact with curriculum
        :param fact: Fact
        :return: None
        """
        if fact.code in self._fact_index:
            message = "Fact {0} already registered".format(fact)
            self._logger.warn(message)
            raise ValueError(message)
        self._fact_index[fact.code] = fact

    def find_competency(self, competency_code):
        """
        Finds competency by code
        :param competency_code: str
        :rtype: knowledge_representation.Competency
        """
        return self._competency_index.get(competency_code, None)

    def find_fact(self, fact_code):
        """
        Finds fact by code
        :param fact_code: str
        :rtype: knowledge_representation.Fact
        """
        return self._fact_index.get(fact_code, None)

    def all_competencies(self):
        return self._competency_index.values()

    def all_facts(self):
        return self._fact_index.values()