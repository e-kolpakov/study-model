from unittest.mock import Mock
import pytest
from agents.base_agents import BaseAgent
from infrastructure.observers import Observer, BaseObserver

__author__ = 'e.kolpakov'


class TestCommonObserver:
    def test_get_observers_attr_missing_returns_empty(self):
        target = Mock(spec="spec that does not have OBSERVER_ATTRIBUTE to prevent creating another mock on access")
        observers = BaseAgent.get_observers(target)
        assert observers == []

    @pytest.mark.parametrize("value", [
        (123,),
        ("123",),
        ([1, 2, 3, 4, 5, 6],),
        ([Observer("", ""), Observer("", ""), Observer("", "")],)
    ])
    def test_get_observers_attr_exists_returns_attr_value(self, value):
        target = Mock()
        setattr(target, BaseObserver.OBSERVER_ATTRIBUTE, value)
        observers = BaseAgent.get_observers(target)
        assert observers == value
