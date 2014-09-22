from agents.student.behaviors.stop_participation import BaseStopParticipationBehavior
from agents.student.behaviors.knowledge_acquisition import BaseFactsAcquisitionBehavior
from agents.student.behaviors.resource_choice import BaseResourceChoiceBehavior
from agents.student.behaviors.study_period import BaseStudyPeriodBehavior
from infrastructure.descriptors import TypedDescriptor


__author__ = 'e.kolpakov'


class BehaviorGroup:
    resource_choice = TypedDescriptor(BaseResourceChoiceBehavior, 'resource_choice')
    knowledge_acquisition = TypedDescriptor(BaseFactsAcquisitionBehavior, 'knowledge_acquisition')
    stop_participation = TypedDescriptor(BaseStopParticipationBehavior, 'stop_participation')
    study_period = TypedDescriptor(BaseStudyPeriodBehavior, 'study_period')

    @classmethod
    def make_group(cls, **kwargs):
        result = cls()
        for behavior_type, behavior in kwargs.items():
            if not hasattr(result, behavior_type):
                raise ValueError("Unknown behavior type {0} specified".format(behavior_type))
            setattr(result, behavior_type, behavior)
        return result