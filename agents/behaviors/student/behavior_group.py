from agents.behaviors.student.stop_participation import BaseStopParticipationBehavior
from agents.behaviors.student.knowledge_acquisition import BaseFactsAcquisitionBehavior
from agents.behaviors.student.resource_choice import BaseResourceChoiceBehavior
from agents.behaviors.student.study_period import BaseStudyPeriodBehavior


__author__ = 'e.kolpakov'


class BehaviorDescriptor:
    def __init__(self, behavior_type, label):
        self._type = behavior_type
        self._lbl = '_'+label

    @property
    def _label(self):
        return self._lbl

    def __get__(self, instance, owner):
        return getattr(instance, self._label, None)

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise ValueError
        setattr(instance, self._label, value)

    def __delete__(self, instance):
        delattr(instance, self._label)


class BehaviorGroup:
    resource_choice = BehaviorDescriptor(BaseResourceChoiceBehavior, 'resource_choice')
    knowledge_acquisition = BehaviorDescriptor(BaseFactsAcquisitionBehavior, 'knowledge_acquisition')
    stop_participation = BehaviorDescriptor(BaseStopParticipationBehavior, 'stop_participation')
    study_period = BehaviorDescriptor(BaseStudyPeriodBehavior, 'study_period')

    @classmethod
    def make_group(cls, **kwargs):
        result = cls()
        for behavior_type, behavior in kwargs.items():
            if not hasattr(result, behavior_type):
                raise ValueError("Unknown behavior type {0} specified".format(behavior_type))
            setattr(result, behavior_type, behavior)
        return result