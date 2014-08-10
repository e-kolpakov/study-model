from weakref import WeakKeyDictionary
from behaviors.student.stop_participation import BaseStopParticipationBehavior
from behaviors.student.knowledge_acquisition import BaseFactsAcquisitionBehavior
from behaviors.student.resource_choice import BaseResourceChoiceBehavior

__author__ = 'e.kolpakov'


class BehaviorDescriptor:
    def __init__(self, behavior_type):
        self._type = behavior_type
        self._data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self._data.get(instance, None)

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise ValueError
        self._data[instance] = value

    def __delete__(self, instance):
        del self._data[instance]


class BehaviorGroup:
    resource_choice = BehaviorDescriptor(BaseResourceChoiceBehavior)
    knowledge_acquisition = BehaviorDescriptor(BaseFactsAcquisitionBehavior)
    stop_participation = BehaviorDescriptor(BaseStopParticipationBehavior)
    # def __init__(self):
    #     self._resource_choice = None
    #     self._knowledge_acquisition = None
    #     self._stop_participation = None
    #
    # @property
    # def resource_choice(self):
    #     """
    #     :rtype: BaseResourceChoiceBehavior
    #     """
    #     return self._resource_choice
    #
    # @resource_choice.setter
    # def resource_choice(self, value):
    #     """
    #     :type value: BaseResourceChoiceBehavior
    #     :rtype: None
    #     """
    #     if not isinstance(value, BaseResourceChoiceBehavior):
    #         raise ValueError
    #     self._resource_choice = value
    #
    # @property
    # def knowledge_acquisition(self):
    #     """
    #     :rtype: BaseFactsAcquisitionBehavior
    #     """
    #     return self._knowledge_acquisition
    #
    # @knowledge_acquisition.setter
    # def knowledge_acquisition(self, value):
    #     """
    #     :type value: BaseFactsAcquisitionBehavior
    #     :rtype: None
    #     """
    #     if not isinstance(value, BaseFactsAcquisitionBehavior):
    #         raise ValueError
    #     self._knowledge_acquisition = value
    #
    # @property
    # def stop_participation(self):
    #     """
    #     :rtype: BaseStopParticipationBehavior
    #     """
    #     return self._stop_participation
    #
    # @stop_participation.setter
    # def stop_participation(self, value):
    #     """
    #     :type value: BaseStopParticipationBehavior
    #     :rtype: None
    #     """
    #     if not isinstance(value, BaseStopParticipationBehavior):
    #         raise ValueError
    #     self._stop_participation = value

    @classmethod
    def make_group(cls, **kwargs):
        result = cls()
        for behavior_type, behavior in kwargs.items():
            if not hasattr(result, behavior_type):
                raise ValueError("Unknown behavior type {0} specified".format(behavior_type))
            setattr(result, behavior_type, behavior)
        return result
