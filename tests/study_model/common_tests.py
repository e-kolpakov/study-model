from unittest import mock, TestCase
from study_model.common import get_available_facts
from study_model.competency import Competency
from study_model.curriculum import Curriculum
from study_model.fact import Fact

__author__ = 'john'


class CommonTests(TestCase):
    def setUp(self):
        self._curriculum = mock.Mock(spec=Curriculum)
        self._curriculum.find_competency_by_fact = mock.Mock(side_effect=self._competency_selector)
        self._competency1 = self._make_competency_mock("c1", ['A', 'B'])
        self._competency2 = self._make_competency_mock("c2", ['C', 'D'], ["c1"])
        self._competency3 = self._make_competency_mock("c3", ['E', 'F'], ["c1", "c2"])

    def _competency_selector(self, fact):
        if fact in self._competency1.facts:
            return self._competency1
        if fact in self._competency2.facts:
            return self._competency2
        if fact in self._competency3.facts:
            return self._competency3
        return None

    def _make_competency_mock(self, code, fact_codes, dependencies=None):
        result = mock.Mock(spec=Competency)
        result.code = code
        result.facts = frozenset([Fact(code) for code in fact_codes])
        result.dependencies = frozenset(dependencies) if dependencies else frozenset()
        return result

    def test_get_available_facts_empty_facts_returns_empty(self):
        facts = set()
        known_facts = frozenset()
        result = get_available_facts(facts, known_facts, self._curriculum)
        self.assertSetEqual(result, set())

    def test_get_available_facts_no_dependencies_returns_facts_as_is(self):
        facts = {Fact('A'), Fact('B')}
        known_facts = frozenset()
        result = get_available_facts(facts, known_facts, self._curriculum)
        self.assertSetEqual(result, facts)

    def test_get_available_facts_factc_depends_on_missing_competency(self):
        self._competency2.dependencies = mock.Mock(return_value=frozenset('c1'))
        result = get_available_facts({Fact('A'), Fact('C')}, frozenset(), self._curriculum)
        self.assertSetEqual(result, {Fact('A')})

    def test_get_available_facts_factb_depends_on_existing_competency(self):
        self._competency1.is_mastered = mock.Mock(return_value=True)

        selector = lambda f: self._competency1 if f == Fact('A') else self._competency2
        self._curriculum.find_competency_by_fact = mock.Mock(side_effect=selector)

        result = get_available_facts({Fact('A'), Fact('B')}, frozenset(), self._curriculum)
        self.assertSetEqual(result, {Fact('A'), Fact('B')})