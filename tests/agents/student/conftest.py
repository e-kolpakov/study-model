from unittest import mock
from unittest.mock import PropertyMock

import pytest
from simpy import Environment

from model.agents.resource import Resource
from model.agents.student import Student
from model.agents.student.behaviors.behavior_group import BehaviorGroup
from model.agents.student.behaviors.knowledge_acquisition import BaseFactsAcquisitionBehavior
from model.agents.student.behaviors.resource_choice import BaseResourceChoiceBehavior
from model.agents.student.behaviors.stop_participation import BaseStopParticipationBehavior
from model.agents.student.behaviors.activity_period import BaseActivityLengthsBehavior
from model.agents.student.behaviors.student_interaction import BaseSendMessagesBehavior
from model.knowledge_representation import Curriculum
from model.knowledge_representation.lesson_type import Lecture
from model.simulation.resource_access import ResourceAccessService


__author__ = 'e.kolpakov'


@pytest.fixture
def behavior_group():
    bhg = mock.Mock(BehaviorGroup)
    bhg.resource_choice = mock.Mock(BaseResourceChoiceBehavior)
    bhg.knowledge_acquisition = mock.Mock(BaseFactsAcquisitionBehavior)
    bhg.stop_participation = mock.Mock(BaseStopParticipationBehavior)
    bhg.study_period = mock.Mock(BaseActivityLengthsBehavior)
    bhg.send_messages = mock.Mock(BaseSendMessagesBehavior)
    return bhg


@pytest.fixture
def env():
    return Environment()


@pytest.fixture
def env_mock():
    return mock.Mock(spec_set=Environment)


@pytest.fixture
def resource_lookup():
    return mock.Mock(spec=ResourceAccessService)


@pytest.fixture
def resource():
    return mock.Mock(spec=Resource)


@pytest.fixture
def lecture():
    fix = mock.Mock(spec=Lecture)
    fix.take = mock.Mock(return_value=True)
    return fix


@pytest.fixture
def student(behavior_group, curriculum, env):
    student_mock = mock.Mock(spec_set=Student)
    student_mock.behavior = PropertyMock(return_value=behavior_group)
    student_mock.env = env
    type(student_mock).curriculum = PropertyMock(return_value=curriculum)
    student_mock.env = env
    return student_mock


@pytest.fixture
def curriculum():
    return mock.Mock(spec_set=Curriculum)