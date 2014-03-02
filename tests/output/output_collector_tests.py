import unittest
from collections import Counter

from pubsub import pub
from output.output_collector import OutputCollector
from output.output_specification.observable import Observable
from output.output_specification.output_specification import OutputSpecification
from output.output_specification.result_record import ResultRecord
from tests.utilities import unordered_equal

__author__ = 'john'


class OutputCollectorTests(unittest.TestCase):

    observable_key1 = "observable1"
    observable_key2 = "observable2"

    observable_name1 = "observable_name1"
    observable_name2 = "observable_name2"

    @staticmethod
    def build_output_collector(observables):
        """
        :param dict[str, str] observables: observable list of type key => name
        :rtype: OutputCollector
        """
        output_spec = OutputSpecification()
        output_spec.observables = [Observable(key, value) for (key, value) in observables.items()]
        return OutputCollector(output_spec)

    def test_single_observable(self):
        collector = OutputCollectorTests.build_output_collector({self.observable_key1: self.observable_name1})

        pub.sendMessage(self.observable_key1, key=self.observable_key1, timestamp=1, value=10.0)

        results = collector.get_results().results

        self.assertEqual(len(results), 1)

        self.assertEqual(results[0], ResultRecord(self.observable_key1, 1, 10.0))

    def test_single_observable_multiple_data(self):
        collector = OutputCollectorTests.build_output_collector({self.observable_key1: self.observable_name1})

        pub.sendMessage(self.observable_key1, key=self.observable_key1, timestamp=1, value=10.0)
        pub.sendMessage(self.observable_key1, key=self.observable_key1, timestamp=2, value=11.0)

        results = collector.get_results().results

        self.assertEqual(len(results), 2)

        self.assertEqual(results[0], ResultRecord(self.observable_key1, 1, 10.0))
        self.assertEqual(results[1], ResultRecord(self.observable_key1, 2, 11.0))

    def test_does_not_capture_unknown_data(self):
        collector = OutputCollectorTests.build_output_collector({self.observable_key1: self.observable_name1})

        pub.sendMessage(self.observable_key2, key=self.observable_key2, timestamp=1, value=10.0)

        results = collector.get_results().results

        self.assertEqual(len(results), 0)

    def test_multiple_observable_single_data(self):
        collector = OutputCollectorTests.build_output_collector({
            self.observable_key1: self.observable_name1,
            self.observable_key2: self.observable_name2,
        })

        pub.sendMessage(self.observable_key1, key=self.observable_key1, timestamp=1, value=10.0)
        pub.sendMessage(self.observable_key2, key=self.observable_key2, timestamp=1, value=0.0)

        expected_results = [ResultRecord(self.observable_key1, 1, 10.0), ResultRecord(self.observable_key2, 1, 0.0)]

        results = collector.get_results().results

        self.assertTrue(unordered_equal(results, expected_results))

    def test_multiple_observable_multiple_data(self):
        collector = OutputCollectorTests.build_output_collector({
            self.observable_key1: self.observable_name1,
            self.observable_key2: self.observable_name2,
        })

        pub.sendMessage(self.observable_key1, key=self.observable_key1, timestamp=1, value=10.0)
        pub.sendMessage(self.observable_key1, key=self.observable_key1, timestamp=2, value=-1.0)
        pub.sendMessage(self.observable_key1, key=self.observable_key1, timestamp=3, value=1.5)
        pub.sendMessage(self.observable_key2, key=self.observable_key2, timestamp=1, value=0.0)
        pub.sendMessage(self.observable_key2, key=self.observable_key2, timestamp=10, value=5.0)
        pub.sendMessage(self.observable_key2, key=self.observable_key2, timestamp=20, value=3.0)

        expected_results = [
            ResultRecord(self.observable_key1, 1, 10.0),
            ResultRecord(self.observable_key1, 2, -1.0),
            ResultRecord(self.observable_key1, 3, 1.5),
            ResultRecord(self.observable_key2, 1, 0.0),
            ResultRecord(self.observable_key2, 10, 5.0),
            ResultRecord(self.observable_key2, 20, 3.0),
        ]

        results = collector.get_results().results

        self.assertTrue(unordered_equal(results, expected_results))





