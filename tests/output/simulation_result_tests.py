import unittest

from nose_parameterized import parameterized
from output.output_specification.result_record import ResultRecord
from output.output_specification.simulation_result import SimulationResult

__author__ = 'john'


class SimulationResultTests(unittest.TestCase):

    simulation_result = None

    result_key1 = 'result_key1'
    result_key2 = 'result_key2'
    result_key3 = 'result_key3'

    std_data = [
        ResultRecord(result_key1, 1, 0.0),
        ResultRecord(result_key1, 2, 5.0),
        ResultRecord(result_key1, 3, 10.0),

        ResultRecord(result_key2, 1, -10.0),
        ResultRecord(result_key2, 2, -5.0),
        ResultRecord(result_key2, 3, 3.0),

        ResultRecord(result_key3, 1, 0.15),
        ResultRecord(result_key3, 2, 0.0),
        ResultRecord(result_key3, 3, -0.1),
    ]

    def setUp(self):
        self.simulation_result = SimulationResult()

    def roll_data(self):
        for data in self.std_data:
            self.simulation_result.register_result(data)

    def test_register_results_actually_register_result(self):
        self.simulation_result.register_result(ResultRecord(self.result_key1, 1, 0.0))
        self.assertEqual(self.simulation_result.results, [ResultRecord(self.result_key1, 1, 0.0)])

        self.simulation_result.register_result(ResultRecord(self.result_key1, 2, 3.0))
        self.assertEqual(self.simulation_result.results, [ResultRecord(self.result_key1, 1, 0.0), ResultRecord(self.result_key1, 2, 3.0)])

        self.simulation_result.register_result(ResultRecord(self.result_key2, 1, 0.0))
        self.assertEqual(self.simulation_result.results, [ResultRecord(self.result_key1, 1, 0.0), ResultRecord(self.result_key1, 2, 3.0), ResultRecord(self.result_key2, 1, 0.0)])

    def test_results_returns_actual_result(self):
        self.roll_data()

        self.assertSequenceEqual(self.simulation_result.results, self.std_data)

    @parameterized.expand([
        ('key1', result_key1),
        ('key2', result_key2),
        ('key3', result_key3),
    ])
    def test_key_slice_returns_correct_data_slice(self, _, key):
        self.roll_data()

        actual_result = list(self.simulation_result.key_slice(key))
        expected_result = [data for data in self.std_data if data.key == key]

        self.assertSequenceEqual(actual_result, expected_result)

    @parameterized.expand([
        ('timestamp1', 1),
        ('timestamp2', 2),
        ('timestamp3', 3),
    ])
    def test_timestamp_slice_returns_correct_data_slice(self, _, timestamp):
        self.roll_data()

        actual_result = list(self.simulation_result.time_slice(timestamp))
        expected_result = [data for data in self.std_data if data.timestamp == timestamp]

        self.assertSequenceEqual(actual_result, expected_result)



