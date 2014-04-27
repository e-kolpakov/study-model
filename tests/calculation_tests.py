import unittest
from nose_parameterized import parameterized
from tests.utils import compare_dicts
from utils.calculations import add_competencies, get_competency_delta

__author__ = 'john'


class CalculationsTests(unittest.TestCase):
    @parameterized.expand([
        ('empty_old', {}, {'a': 1.0, 'b': 0.6}, {'a': 1.0, 'b': 0.6}),
        ('distinct', {'a': 0.5}, {'b': 0.3}, {'b': 0.3}),
        ('adds_matched', {'a': 0.5, 'b': 0.3}, {'a': 0.3, 'b': 0.7}, {'a': 0.8, 'b': 1.0}),
        ('adds_up_to_one', {'a': 0.8, 'b': 1.0}, {'a': 0.3, 'b': 0.5}, {'a': 1.0, 'b': 1.0})
    ])
    def test_add_competencies_only_new_true(self, _, old, new, expected):
        self.assertDictEqual(add_competencies(old, new, new_only=True), expected)

    @parameterized.expand([
        ('empty_old', {}, {'a': 1.0, 'b': 0.6}, {'a': 1.0, 'b': 0.6}),
        ('distinct', {'a': 0.5}, {'b': 0.3}, {'a': 0.5, 'b': 0.3}),
        ('appends_not_matched', {'a': 0.5, 'b': 0.5}, {'b': 0.3}, {'a': 0.5, 'b': 0.8}),
    ])
    def test_add_competencies_only_new_false(self, _, old, new, expected):
        self.assertDictEqual(add_competencies(old, new, new_only=False), expected)

    @parameterized.expand([
        ('empty_old', {}, {'a': 0.5}, {'a': 0.5}),
        ('distinct', {'a': 0.5}, {'b': 0.5}, {'b': 0.5}),
        ('subtracts_matched', {'a': 0.5}, {'a': 0.7, 'b': 0.2}, {'a': 0.2, 'b': 0.2}),
        ('subtracts_to_zero', {'a': 0.5, 'b': 0.2}, {'a': 0.3, 'b': 0.2}, {'a': 0.0, 'b': 0.0})
    ])
    def test_get_competency_delta_only_new_true(self, _, old, new, expected):
        result = get_competency_delta(new, old, only_new=True)
        compare_dicts(result, expected, self.assertAlmostEqual)

    @parameterized.expand([
        ('empty_old', {}, {'a': 0.5}, {'a': 0.5}),
        ('distinct', {'a': 0.5}, {'b': 0.3}, {'a': 0.0, 'b': 0.3}),
        ('appends_not_matched_with_zero', {'a': 0.5, 'b': 0.2}, {'b': 0.3}, {'a': 0.0, 'b': 0.1}),
    ])
    def test_get_competency_delta_only_new_false(self, _, old, new, expected):
        result = get_competency_delta(new, old, only_new=False)
        compare_dicts(result, expected, self.assertAlmostEqual)