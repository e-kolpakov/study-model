from agents.behaviors.student.resource_choice import BaseResourceChoiceBehavior

__author__ = 'john'


class BehaviorGroup:
    def __init__(self):
        self._resource_choice = None

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