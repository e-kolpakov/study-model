from unittest import mock

import pytest

from model.agents.student import Student


__author__ = 'e.kolpakov'


@pytest.fixture
def student():
    return mock.Mock(spec=Student)