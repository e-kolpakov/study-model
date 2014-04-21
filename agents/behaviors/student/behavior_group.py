from agents.behaviors.student.knowledge_acquisition import BaseKnowledgeAcquisitionBehavior
from agents.behaviors.student.resource_choice import BaseResourceChoiceBehavior

__author__ = 'john'


class BehaviorGroup:
    def __init__(self):
        self._resource_choice = None
        self._knowledge_acquisistion = None

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
        :rtype: BaseKnowledgeAcquisitionBehavior
        """
        return self._knowledge_acquisistion

    @knowledge_acquisition.setter
    def knowledge_acquisition(self, value):
        """
        :type value: BaseKnowledgeAcquisitionBehavior
        :rtype: None
        """
        if not isinstance(value, BaseKnowledgeAcquisitionBehavior):
            raise ValueError
        self._knowledge_acquisistion = value