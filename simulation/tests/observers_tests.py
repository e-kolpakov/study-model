from unittest import TestCase
from unittest.mock import Mock, patch

from nose_parameterized import parameterized

from simulation.observers import get_observers, Observer, BaseObserver, DeltaObserver


__author__ = 'e.kolpakov'


class CommonObserverTests(TestCase):
    def test_get_observers_attr_missing_returns_empty(self):
        target = Mock(spec="spec that does not have OBSERVER_ATTRIBUTE to prevent creating another mock on access")
        observers = get_observers(target)
        self.assertEqual(observers, [])

    @parameterized.expand([
        (123,),
        ("123",),
        ([1, 2, 3, 4, 5, 6],),
        ([Observer("", ""), Observer("", ""), Observer("", "")],)
    ])
    def test_get_observers_attr_exists_returns_attr_value(self, value):
        target = Mock()
        setattr(target, BaseObserver.OBSERVER_ATTRIBUTE, value)
        observers = get_observers(target)
        self.assertEqual(observers, value)


class ObserverTests(TestCase):
    def test_observe_missing_topic_throws_value_error(self):
        self.assertRaises(ValueError, lambda: Observer.observe(""))

    def test_observe_registers_observer(self):
        mock = Mock()
        decorator = Observer.observe("Topic")
        decorated = decorator(mock)
        self.assertTrue(hasattr(decorated, Observer.OBSERVER_ATTRIBUTE))
        observers = getattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        self.assertEqual(type(observers), list)
        self.assertEqual(len(observers), 1)
        observer = observers[0]
        self.assertEqual(type(observer), Observer)
        self.assertEqual(observer.topic, "Topic")

    def test_observe_keeps_existing_observers(self):
        mock = Mock()
        decorator1 = Observer.observe("Topic1")
        decorator2 = Observer.observe("Topic2")
        decorated = decorator1(mock)
        decorated = decorator2(decorated)
        observers = getattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        self.assertEqual(type(observers), list)
        self.assertEqual(len(observers), 2)
        observer1, observer2 = observers
        self.assertEqual(type(observer1), Observer)
        self.assertEqual(observer1.topic, "Topic1")
        self.assertEqual(type(observer2), Observer)
        self.assertEqual(observer2.topic, "Topic2")

    @parameterized.expand([
        ("SomeTopic", "Smith", 1, None, 1),
        ("OtherTopic", "Carter", 2, lambda x: x ** 2, 15),
        ("YetAnotherTopic", "Fury", 3, lambda x: x.upper(), "qwe"),
    ])
    def test_inspect_sends_message(self, topic, agent, step_number, converter, value):
        eff_converter = converter if converter else lambda x: x
        mock = Mock(return_value=value)
        decorated = Observer.observe(topic, converter=converter)(mock)
        observer = get_observers(decorated)[0]
        with patch('simulation.observers.pub.sendMessage', spec=True) as pub_mock:
            observer.inspect(agent, step_number)
            expected_value = eff_converter(value)
            pub_mock.assert_called_once_with(topic, agent=agent, step_number=step_number, value=expected_value)


class DeltaObserverTests(TestCase):
    def test_observe_missing_topic_throws_value_error(self):
        self.assertRaises(ValueError, lambda: DeltaObserver.observe(""))

    def test_observe_missing_delta_throws_value_error(self):
        self.assertRaises(ValueError, lambda: DeltaObserver.observe("SomeTopic"))

    def test_observe_registers_observer(self):
        mock = Mock()
        decorator = DeltaObserver.observe("Topic", delta=lambda x, y: x-y)
        decorated = decorator(mock)
        self.assertTrue(hasattr(decorated, Observer.OBSERVER_ATTRIBUTE))
        observers = getattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        self.assertEqual(type(observers), list)
        self.assertEqual(len(observers), 1)
        observer = observers[0]
        self.assertEqual(type(observer), DeltaObserver)
        self.assertEqual(observer.topic, "Topic")

    def test_observe_keeps_existing_observers(self):
        mock = Mock()
        decorator1 = DeltaObserver.observe("Topic1", delta=lambda x,y: x-y)
        decorator2 = DeltaObserver.observe("Topic2", delta=lambda x,y: x-y)
        decorated = decorator1(mock)
        decorated = decorator2(decorated)
        observers = getattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        self.assertEqual(type(observers), list)
        self.assertEqual(len(observers), 2)
        observer1, observer2 = observers
        self.assertEqual(type(observer1), DeltaObserver)
        self.assertEqual(observer1.topic, "Topic1")
        self.assertEqual(type(observer2), DeltaObserver)
        self.assertEqual(observer2.topic, "Topic2")

    @parameterized.expand([
        ("SomeTopic", "Smith", 1, None, lambda x, y: x-y, 10, 20),  # 20-10
        ("OtherTopic", "Carter", 2, lambda x: x ** 2, lambda x, y: x+y, 15, 16),  # 15**2+16**2
        ("YetAnotherTopic", "Fury", 3, lambda x: x.upper(), lambda x, y: x+y, "qwe", "asd"),  # "qwe"+"asd"
    ])
    def test_inspect_sends_message(self, topic, agent, step_number, converter, delta, value1, value2):
        eff_converter = converter if converter else lambda x: x
        mock = Mock(return_value=value1)
        decorated = DeltaObserver.observe(topic, converter=converter, delta=delta)(mock)
        observer = get_observers(decorated)[0]
        with patch('simulation.observers.pub.sendMessage', spec=True) as pub_mock:
            expected_delta1 = eff_converter(value1)

            observer.inspect(agent, step_number)
            pub_mock.assert_called_with(topic, agent=agent, step_number=step_number, delta=expected_delta1)

            mock.return_value = value2
            expected_delta2 = delta(eff_converter(value2), eff_converter(value1))

            observer.inspect(agent, step_number)
            pub_mock.assert_called_with(topic, agent=agent, step_number=step_number, delta=expected_delta2)