from knowledge_representation import Fact, get_available_facts


__author__ = 'e.kolpakov'


def test_get_available_facts_empty_facts_returns_empty():
    facts = set()
    known_facts = frozenset()
    result = get_available_facts(facts, known_facts)
    assert result == set()


def test_get_available_facts_no_dependencies_returns_facts_as_is():
    facts = {Fact('A'), Fact('B')}
    known_facts = frozenset()
    result = get_available_facts(facts, known_facts)
    assert result == facts


def test_get_available_facts_factc_depends_on_missing_fact():
    facts = {Fact('A'), Fact('C', ['B'])}
    result = get_available_facts(facts, frozenset())
    assert result == {Fact('A')}


def test_get_available_facts_factb_depends_on_existing_competency():
    facts = {Fact('B', ['A'])}
    result = get_available_facts(facts, frozenset([Fact('A')]))
    assert result == facts


def test_get_available_facts_factb_depends_on_fact_in_same_set():
    facts = {Fact('A'), Fact('B', ['A'])}
    result = get_available_facts(facts, frozenset())
    assert result == facts


def test_get_available_facts_dependency_chain_on_same_set():
    facts = {Fact('A'), Fact('B', ['A']), Fact('C', ['B'])}
    result = get_available_facts(facts, frozenset())
    assert result == facts


def test_get_available_facts_removes_all_known_facts():
    facts = {Fact('A'), Fact('B'), Fact('C'), Fact('D')}
    known = frozenset([Fact('A'), Fact('B'), Fact('C')])
    result = get_available_facts(facts, known)
    assert result == {Fact('D')}