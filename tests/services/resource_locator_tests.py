import unittest
from src.services.resource_locator import ResourceLocator

__author__ = 'john'


class TestClass(object):
    def __eq__(self, other):
        if not isinstance(other, TestClass):
            return False
        return self.a == other.a and self.b == other.b

    def __init__(self, a, b):
        self.a = a
        self.b = b


class ResourceLocatorTests(unittest.TestCase):

    resource_locator = None

    def setUp(self):
        self.resource_locator = ResourceLocator()

    def test_register_instance_type_parameter_is_not_type_raises_value_error(self):
        self.assertRaises(ValueError, lambda: self.resource_locator.register_instance(10, 11))
        self.assertRaises(ValueError, lambda: self.resource_locator.register_instance("qweqweqwe", 11))

    def test_register_instance_parameter_is_not_of_instance_type_raises_value_error(self):
        self.assertRaises(ValueError, lambda: self.resource_locator.register_instance(int, "test"))
        self.assertRaises(ValueError, lambda: self.resource_locator.register_instance(str, 11))
        self.assertRaises(ValueError, lambda: self.resource_locator.register_instance(str, 11))

    def test_register_does_not_raise(self):
        self.resource_locator.register_instance(int, 10)
        self.resource_locator.register_instance(str, "qwerty", "string_key")
        self.resource_locator.register_instance(str, "qwerty", 12)
        self.resource_locator.register_instance(TestClass, TestClass(1, 2))
        self.resource_locator.register_instance(TestClass, TestClass(1, 2), "string_key")
        self.resource_locator.register_instance(TestClass, TestClass(1, 2), 15)

    def test_get_instance_returns_empty_list_if_empty(self):
        resolved = self.resource_locator.get_instances(int)
        self.assertSequenceEqual(resolved, list())

    def test_get_instance_returns_correct_instance_no_key(self):
        self.resource_locator.register_instance(int, 10)

        resolved = self.resource_locator.get_instances(int)

        self.assertSequenceEqual(resolved, [10,])

    def test_get_instance_returns_correct_instances_no_key(self):
        self.resource_locator.register_instance(int, 10)
        self.resource_locator.register_instance(TestClass, TestClass(1, 2))
        self.resource_locator.register_instance(TestClass, TestClass(3, 4))

        resolved = self.resource_locator.get_instances(TestClass)

        self.assertSequenceEqual(resolved, [TestClass(1, 2), TestClass(3, 4)])

    def test_get_instance_returns_correct_instances_with_key(self):
        self.resource_locator.register_instance(int, 1, "qwerty")
        self.resource_locator.register_instance(int, 2, "qwerty")
        self.resource_locator.register_instance(int, 12, 15)

        resolved = self.resource_locator.get_instances(int, "qwerty")

        self.assertSequenceEqual(resolved, [1, 2])