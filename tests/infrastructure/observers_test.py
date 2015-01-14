from unittest.mock import Mock, patch

import pytest

from model.agents.base_agents import BaseAgent
from model.infrastructure.observers import (
    Observer, DeltaObserver, CallObserver, AgentCallObserver, get_observers, BaseObserver
)


__author__ = 'e.kolpakov'


class TestCommonObserver:
    def test_get_observers_attr_missing_returns_empty(self):
        target = Mock(spec="spec that does not have OBSERVER_ATTRIBUTE to prevent creating another mock on access")
        observers = get_observers(target)
        assert observers == []

    @pytest.mark.parametrize("value", [
        ([Observer("", ""), DeltaObserver("", "", "")]),
        ([Observer("", ""), Observer("", ""), Observer("", "")])
    ])
    def test_get_observers_attr_exists_returns_attr_value(self, value):
        target = Mock()
        setattr(target, BaseObserver.OBSERVER_ATTRIBUTE, value)
        observers = get_observers(target)
        assert observers == value


class TestObserver:
    def test_observe_missing_topic_throws_value_error(self):
        with pytest.raises(ValueError):
            Observer.observe("")

    def test_observe_registers_observer(self):
        mock = Mock()
        decorator = Observer.observe("Topic")
        decorated = decorator(mock)
        assert hasattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        observers = getattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        assert type(observers) == list
        assert len(observers) == 1
        observer = observers[0]
        assert type(observer) == Observer
        assert observer.topic == "Topic"

    def test_observe_keeps_existing_observers(self):
        mock = Mock()
        decorator1 = Observer.observe("Topic1")
        decorator2 = Observer.observe("Topic2")
        decorated = decorator1(mock)
        decorated = decorator2(decorated)
        observers = getattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        assert type(observers) == list
        assert len(observers) == 2
        observer1, observer2 = observers
        assert type(observer1) == Observer
        assert observer1.topic == "Topic1"
        assert type(observer2) == Observer
        assert observer2.topic == "Topic2"

    @pytest.mark.parametrize("topic, agent, converter, value", [
        ("SomeTopic", "Smith", None, 1),
        ("OtherTopic", "Carter", lambda x: x ** 2, 15),
        ("YetAnotherTopic", "Fury", lambda x: x.upper(), "qwe"),
    ])
    def test_inspect_sends_message(self, topic, agent, converter, value):
        eff_converter = converter if converter else lambda x: x
        mock = Mock(return_value=value)
        decorated = Observer.observe(topic, converter=converter)(mock)
        observer = get_observers(decorated)[0]
        with patch('infrastructure.observers.pub.sendMessage', spec=True) as pub_mock:
            observer.inspect(agent)
            expected_value = eff_converter(value)
            pub_mock.assert_called_once_with(topic, agent=agent, value=expected_value)


class TestDeltaObserver:
    def test_observe_missing_topic_throws_value_error(self):
        with pytest.raises(ValueError):
            DeltaObserver.observe("")

    def test_observe_missing_delta_throws_value_error(self):
        with pytest.raises(ValueError):
            DeltaObserver.observe("SomeTopic")

    def test_observe_registers_observer(self):
        mock = Mock()
        decorator = DeltaObserver.observe("Topic", delta=lambda x, y: x - y)
        decorated = decorator(mock)
        assert hasattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        observers = getattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        assert type(observers) == list
        assert len(observers) == 1
        observer = observers[0]
        assert type(observer) == DeltaObserver
        assert observer.topic == "Topic"

    def test_observe_keeps_existing_observers(self):
        mock = Mock()
        decorator1 = DeltaObserver.observe("Topic1", delta=lambda x, y: x - y)
        decorator2 = DeltaObserver.observe("Topic2", delta=lambda x, y: x - y)
        decorated = decorator1(mock)
        decorated = decorator2(decorated)
        observers = getattr(decorated, Observer.OBSERVER_ATTRIBUTE)
        assert type(observers) == list
        assert len(observers) == 2
        observer1, observer2 = observers
        assert type(observer1) == DeltaObserver
        assert observer1.topic == "Topic1"
        assert type(observer2) == DeltaObserver
        assert observer2.topic == "Topic2"

    @pytest.mark.parametrize("topic, agent, converter, delta, value1, value2", [
        ("SomeTopic", "Smith", None, lambda x, y: x - y, 10, 20),  # 20-10
        ("OtherTopic", "Carter", lambda x: x ** 2, lambda x, y: x + y, 15, 16),  # 15**2+16**2
        ("YetAnotherTopic", "Fury", lambda x: x.upper(), lambda x, y: x + y, "qwe", "asd"),  # "qwe"+"asd"
    ])
    def test_inspect_sends_message(self, topic, agent, converter, delta, value1, value2):
        eff_converter = converter if converter else lambda x: x
        mock = Mock(return_value=value1)
        decorated = DeltaObserver.observe(topic, converter=converter, delta=delta)(mock)
        observer = get_observers(decorated)[0]
        with patch('infrastructure.observers.pub.sendMessage', spec=True) as pub_mock:
            expected_delta1 = eff_converter(value1)

            observer.inspect(agent)
            pub_mock.assert_called_with(topic, agent=agent, delta=expected_delta1)

            mock.return_value = value2
            expected_delta2 = delta(eff_converter(value2), eff_converter(value1))

            observer.inspect(agent)
            pub_mock.assert_called_with(topic, agent=agent, delta=expected_delta2)


class TestCallObserverTest:
    @pytest.mark.parametrize("topic, args, kwargs", [
        ("Topic1", tuple(), dict()),
        ("Topic2", (1,), dict()),
        ("Topic3", (1, 2, 3), {"kwarg1": 1, "kwarg2": 2}),
    ])
    def test_observe_sends_message_on_target_call(self, topic, args, kwargs):  # not a typo, actual list and dict
        target = Mock()
        decorated = CallObserver.observe(topic)(target)
        with patch('infrastructure.observers.pub.sendMessage', spec=True) as pub_mock:
            decorated(*args, **kwargs)
            pub_mock.assert_called_with(topic, args=args, kwargs=kwargs)


class TestAgentCallObserver:
    @pytest.mark.parametrize("topic, time, args, kwargs", [
        ("Topic1", 1, tuple(), dict()),
        ("Topic2", 2, (1,), dict()),
        ("Topic3", 3, (1, 2, 3), {"kwarg1": 1, "kwarg2": 2}),
    ])
    # not a typo, args should not be *args, kwargs should not be **kwargs
    def test_observe_sends_message_on_target_call(self, topic, time, args, kwargs):
        target = Mock()
        agent_mock = Mock(spec=BaseAgent)
        agent_mock.time = time
        decorated = AgentCallObserver.observe(topic)(target)
        actual_args = tuple([agent_mock] + list(args))
        with patch('infrastructure.observers.pub.sendMessage', spec=True) as pub_mock:
            decorated(*actual_args, **kwargs)
            pub_mock.assert_called_with(topic, agent=agent_mock, args=args, kwargs=kwargs)