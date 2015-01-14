from copy import deepcopy

from .curriculum import Curriculum
from .fact import Fact, Competency

__author__ = 'e.kolpakov'


def get_available_facts(facts, known_facts):
    """
    :param facts: frozenset[Fact]
    :param known_facts: frozenset[Fact]
    :rtype: frozenset[knowledge_representation.fact.Fact]
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
        new_available = set(fact_to_check for fact_to_check in to_check if fact_to_check.is_available(available))

    return frozenset(available & facts - known_facts)