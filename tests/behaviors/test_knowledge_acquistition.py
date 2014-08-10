from unittest import mock

import pytest

from agents import Resource, Student
from behaviors.student.knowledge_acquisition import AllDependenciesAcquisitionBehavior, GetAllFactsAcquisitionBehavior
from knowledge_representation import Fact, ResourceFact


__author__ = 'e.kolpakov'


def _to_resource_fact(facts):
    return tuple([ResourceFact(fact) for fact in facts])


@pytest.fixture
def student(knowledge_mock):
    s = mock.MagicMock(spec=Student)
    type(s).knowledge = knowledge_mock
    return s


@pytest.fixture
def resource(facts_mock):
    res = mock.MagicMock(spec=Resource)
    type(res).facts = facts_mock
    return res


@pytest.fixture
def facts_mock():
    return mock.PropertyMock()


@pytest.fixture
def knowledge_mock():
    return mock.PropertyMock()


class TestGetAllFactsAcquisitionBehavior:
    @pytest.fixture
    def behavior(self):
        return GetAllFactsAcquisitionBehavior()

    def test_no_facts_returns_empty(self, student, resource, behavior, facts_mock):
        facts_mock.return_value = []

        result = behavior.acquire_facts(student, resource)

        assert result == set()

    def test_turns_resource_facts_into_facts(self, student, resource, behavior, facts_mock):
        facts = {Fact('A'), Fact('B'), Fact('C')}
        facts_mock.return_value = _to_resource_fact(facts)

        result = behavior.acquire_facts(student, resource)

        assert result == facts


class TestAllDependenciesAcquisitionBehavior:
    @pytest.fixture
    def behavior(self):
        return AllDependenciesAcquisitionBehavior()

    def test_no_facts_returns_empty(self, student, resource, behavior, facts_mock, knowledge_mock):
        facts_mock.return_value = []
        knowledge_mock.return_value = frozenset()

        result = behavior.acquire_facts(student, resource)

        assert result == set()

    def test_turns_resource_facts_into_facts(self, student, resource, behavior, facts_mock, knowledge_mock):
        facts = {Fact('A'), Fact('B'), Fact('C')}
        facts_mock.return_value = _to_resource_fact(facts)
        knowledge_mock.return_value = frozenset()

        result = behavior.acquire_facts(student, resource)

        assert result == facts

    def test_filters_facts_with_missing_dependencies(self, student, resource, behavior, facts_mock, knowledge_mock):
        facts = {Fact('A'), Fact('C', ['B'])}
        facts_mock.return_value = _to_resource_fact(facts)
        knowledge_mock.return_value = frozenset()

        result = behavior.acquire_facts(student, resource)

        assert result == {Fact('A')}