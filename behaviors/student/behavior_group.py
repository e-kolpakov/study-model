from behaviors.student.knowledge_acquisition import BaseFactsAcquisitionBehavior
from behaviors.student.resource_choice import BaseResourceChoiceBehavior

__author__ = 'e.kolpakov'


class BehaviorGroup:
    def __init__(self):
        self._resource_choice = None
        self._knowledge_acquisition = None

    @property
    def resource_choice(self):
        """
        :rtype: BaseResourceChoiceBehavior
        """
        return self._resource_choice

    @resource_choice.setter
    def resource_choice(self, value):
        """
        :type value: BaseResourceChoiceBehavior
        :rtype: None
        """
        if not isinstance(value, BaseResourceChoiceBehavior):
            raise ValueError
        self._resource_choice = value

    @property
    def knowledge_acquisition(self):
        """
        :rtype: BaseFactsAcquisitionBehavior
        """
        return self._knowledge_acquisition

    @knowledge_acquisition.setter
    def knowledge_acquisition(self, value):
        """
        :type value: BaseFactsAcquisitionBehavior
        :rtype: None
        """
        if not isinstance(value, BaseFactsAcquisitionBehavior):
            raise ValueError
        self._knowledge_acquisition = value