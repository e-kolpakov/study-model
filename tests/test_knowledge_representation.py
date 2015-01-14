import pytest

from model.knowledge_representation import Competency, Fact, Curriculum, get_available_facts

__author__ = 'e.kolpakov'


class TestCurriculum:
    @pytest.fixture
    def curriculum(self):
        return Curriculum()

    def test_empty_curriculum_all_lookups_return_none(self, curriculum):
        assert curriculum.find_competency("qwe") is None
        assert curriculum.find_fact("qwe") is None

    def test_register_competency_can_lookup_by_code(self, curriculum):
        comp1 = Competency('qwe', [])
        comp2 = Competency('zxc', [])
        curriculum.register_competency(comp1)
        curriculum.register_competency(comp2)

        assert curriculum.find_competency('qwe') == comp1
        assert curriculum.find_competency('zxc') == comp2

    def test_register_fact_can_lookup_fact_by_code(self, curriculum):
        for fact in [Fact("A"), Fact("B"), Fact("C"), Fact("D")]:
            curriculum.register_fact(fact)

        assert curriculum.find_fact("A") == Fact("A")
        assert curriculum.find_fact("B") == Fact("B")
        assert curriculum.find_fact("C") == Fact("C")
        assert curriculum.find_fact("D") == Fact("D")

        assert curriculum.find_fact("Z") is None


class TestGetAvailableFacts:
    def test_get_available_facts_empty_facts_returns_empty(self):
        facts = set()
        known_facts = frozenset()
        result = get_available_facts(facts, known_facts)
        assert result == set()

    def test_get_available_facts_no_dependencies_returns_facts_as_is(self):
        facts = {Fact('A'), Fact('B')}
        known_facts = frozenset()
        result = get_available_facts(facts, known_facts)
        assert result == facts

    def test_get_available_facts_factc_depends_on_missing_fact(self):
        facts = {Fact('A'), Fact('C', ['B'])}
        result = get_available_facts(facts, frozenset())
        assert result == {Fact('A')}

    def test_get_available_facts_factb_depends_on_existing_competency(self):
        facts = {Fact('B', ['A'])}
        result = get_available_facts(facts, frozenset([Fact('A')]))
        assert result == facts

    def test_get_available_facts_factb_depends_on_fact_in_same_set(self):
        facts = {Fact('A'), Fact('B', ['A'])}
        result = get_available_facts(facts, frozenset())
        assert result == facts

    def test_get_available_facts_dependency_chain_on_same_set(self):
        facts = {Fact('A'), Fact('B', ['A']), Fact('C', ['B'])}
        result = get_available_facts(facts, frozenset())
        assert result == facts

    def test_get_available_facts_removes_all_known_facts(self):
        facts = {Fact('A'), Fact('B'), Fact('C'), Fact('D')}
        known = frozenset([Fact('A'), Fact('B'), Fact('C')])
        result = get_available_facts(facts, known)
        assert result == {Fact('D')}