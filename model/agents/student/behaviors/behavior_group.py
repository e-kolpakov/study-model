from model.agents.student.behaviors.stop_participation import BaseStopParticipationBehavior
from model.agents.student.behaviors.knowledge_acquisition import BaseFactsAcquisitionBehavior
from model.agents.student.behaviors.resource_choice import BaseResourceChoiceBehavior
from model.agents.student.behaviors.student_interaction import BaseSendMessagesBehavior
from model.agents.student.behaviors.activity_period import BaseActivityLengthsBehavior
from model.infrastructure.descriptors import TypedDescriptor


__author__ = 'e.kolpakov'


class BehaviorGroup:
    resource_choice = TypedDescriptor(BaseResourceChoiceBehavior, 'resource_choice')
    knowledge_acquisition = TypedDescriptor(BaseFactsAcquisitionBehavior, 'knowledge_acquisition')
    stop_participation = TypedDescriptor(BaseStopParticipationBehavior, 'stop_participation')
    activity_periods = TypedDescriptor(BaseActivityLengthsBehavior, 'activity_periods')
    send_messages = TypedDescriptor(BaseSendMessagesBehavior, 'send_messages')

    @classmethod
    def make_group(cls, **kwargs):
        result = cls()
        for behavior_type, behavior in kwargs.items():
            if not hasattr(result, behavior_type):
                raise ValueError("Unknown behavior type {0} specified".format(behavior_type))
            setattr(result, behavior_type, behavior)
        return result