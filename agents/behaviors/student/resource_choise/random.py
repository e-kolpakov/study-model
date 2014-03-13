import random
from agents.behaviors.student.resource_choise.base import BaseResourceChoiceBehavior

__author__ = 'john'


class RandomResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def choose_resource(self, student, available_resources):
        """
        :type student: Student
        :type available_resources: list[Resource]
        :rtype: Resource
        """
        return random.choice(available_resources)