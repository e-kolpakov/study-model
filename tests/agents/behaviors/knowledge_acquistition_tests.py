import unittest
from unittest import mock

from behaviors.student.knowledge_acquisition import AllDependenciesAcquisitionBehavior, \
    GetAllFactsAcquisitionBehavior
from agents.resource import Resource
from agents.student import Student
from study_model.fact import Fact, ResourceFact


__author__ = 'e.kolpakov'


def _to_resource_fact(facts):
    return tuple([ResourceFact(fact) for fact in facts])


class GetAllFactsAcquisitionBehaviorTests(unittest.TestCase):
    def setUp(self):
        self._behavior = GetAllFactsAcquisitionBehavior()
        self._student = mock.MagicMock(spec=Student)
        self._resource = mock.MagicMock(spec=Resource)
        self._factsMock = mock.PropertyMock()
        type(self._resource).facts = self._factsMock

    def test_no_facts_returns_empty(self):
        self._factsMock.return_value = []

        result = self._behavior.acquire_facts(self._student, self._resource)

        self.assertSetEqual(result, set())

    def test_turns_resource_facts_into_facts(self):
        facts = {Fact('A'), Fact('B'), Fact('C')}
        self._factsMock.return_value = _to_resource_fact(facts)

        result = self._behavior.acquire_facts(self._student, self._resource)

        self.assertSetEqual(result, facts)


class AllDependenciesAcquisitionBehaviorTests(unittest.TestCase):
    def setUp(self):
        self._behavior = AllDependenciesAcquisitionBehavior()
        self._student = mock.MagicMock(spec=Student)
        self._resource = mock.MagicMock(spec=Resource)
        self._factsMock = mock.PropertyMock()
        type(self._resource).facts = self._factsMock
        self._knowledgeMock = mock.PropertyMock()
        type(self._student).knowledge = self._knowledgeMock

    def test_no_facts_returns_empty(self):
        self._factsMock.return_value = []
        self._knowledgeMock.return_value = frozenset()

        result = self._behavior.acquire_facts(self._student, self._resource)

        self.assertSetEqual(result, set())

    def test_turns_resource_facts_into_facts(self):
        facts = {Fact('A'), Fact('B'), Fact('C')}
        self._factsMock.return_value = _to_resource_fact(facts)
        self._knowledgeMock.return_value = frozenset()

        result = self._behavior.acquire_facts(self._student, self._resource)

        self.assertSetEqual(result, facts)

    def test_filters_facts_with_missing_dependencies(self):
        facts = {Fact('A'), Fact('C', ['B'])}
        self._factsMock.return_value = _to_resource_fact(facts)
        self._knowledgeMock.return_value = frozenset()

        result = self._behavior.acquire_facts(self._student, self._resource)

        self.assertSetEqual(result, {Fact('A')})