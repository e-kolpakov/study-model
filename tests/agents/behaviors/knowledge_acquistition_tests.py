import unittest
from unittest import mock
from agents.behaviors import GetAllFactsAcquisitionBehavior
from agents.resource import Resource
from agents.student import Student
from study_model.fact import Fact, ResourceFact

__author__ = 'john'


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
        resource_facts = tuple([ResourceFact(fact) for fact in facts])
        self._factsMock.return_value = resource_facts
        result = self._behavior.acquire_facts(self._student, self._resource)
        self.assertSetEqual(result, facts)
