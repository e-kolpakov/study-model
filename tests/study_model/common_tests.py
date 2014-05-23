from unittest import mock, TestCase

from study_model.common import get_available_facts
from study_model.competency import Competency
from study_model.curriculum import Curriculum
from study_model.fact import Fact


__author__ = 'e.kolpakov'


class CommonTests(TestCase):
    def setUp(self):
        self._curriculum = mock.Mock(spec=Curriculum)

    def _make_competency_mock(self, code, fact_codes, dependencies=None):
        result = mock.Mock(spec=Competency)
        result.code = code
        result.facts = frozenset([Fact(code) for code in fact_codes])
        result.dependencies = frozenset(dependencies) if dependencies else frozenset()
        return result

    def test_get_available_facts_empty_facts_returns_empty(self):
        facts = set()
        known_facts = frozenset()
        result = get_available_facts(facts, known_facts)
        self.assertSetEqual(result, set())

    def test_get_available_facts_no_dependencies_returns_facts_as_is(self):
        facts = {Fact('A'), Fact('B')}
        known_facts = frozenset()
        result = get_available_facts(facts, known_facts)
        self.assertSetEqual(result, facts)

    def test_get_available_facts_factc_depends_on_missing_fact(self):
        facts = {Fact('A'), Fact('C', ['B'])}
        result = get_available_facts(facts, frozenset())
        self.assertSetEqual(result, {Fact('A')})

    def test_get_available_facts_factb_depends_on_existing_competency(self):
        facts = {Fact('B', ['A'])}
        result = get_available_facts(facts, frozenset([Fact('A')]))
        self.assertSetEqual(result, facts)

    def test_get_available_facts_factb_depends_on_fact_in_same_set(self):
        facts = {Fact('A'), Fact('B', ['A'])}
        result = get_available_facts(facts, frozenset())
        self.assertSetEqual(result, facts)

    def test_get_available_facts_dependency_chain_on_same_set(self):
        facts = {Fact('A'), Fact('B', ['A']), Fact('C', ['B'])}
        result = get_available_facts(facts, frozenset())
        self.assertSetEqual(result, facts)

    def test_get_available_facts_removes_all_known_facts(self):
        facts = {Fact('A'), Fact('B'), Fact('C'), Fact('D')}
        known = frozenset([Fact('A'), Fact('B'), Fact('C')])
        result = get_available_facts(facts, known)
        self.assertSetEqual(result, {Fact('D')})