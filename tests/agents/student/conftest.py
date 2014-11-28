from unittest import mock

import pytest
from simpy import Environment

from agents.resource import Resource
from agents.student.behaviors.behavior_group import BehaviorGroup
from agents.student.behaviors.knowledge_acquisition import BaseFactsAcquisitionBehavior
from agents.student.behaviors.resource_choice import BaseResourceChoiceBehavior
from agents.student.behaviors.stop_participation import BaseStopParticipationBehavior
from agents.student.behaviors.study_period import BaseActivityLengthsBehavior
from knowledge_representation.lesson_type import Lecture
from simulation.resource_access import ResourceAccessService


__author__ = 'e.kolpakov'

@pytest.fixture
def behavior_group():
    bhg = mock.Mock(BehaviorGroup)
    bhg.resource_choice = mock.Mock(BaseResourceChoiceBehavior)
    bhg.knowledge_acquisition = mock.Mock(BaseFactsAcquisitionBehavior)
    bhg.stop_participation = mock.Mock(BaseStopParticipationBehavior)
    bhg.study_period = mock.Mock(BaseActivityLengthsBehavior)
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