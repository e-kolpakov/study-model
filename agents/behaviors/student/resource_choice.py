import random
from agents.behaviors.base_behavior import BaseBehavior

__author__ = 'john'


class BaseResourceChoiceBehavior(BaseBehavior):
    def __init__(self):
        super().__init__()

    def choose_resource(self, student, available_resources):
        """
        :type student: Student
        :type available_resources: tuple[Resource]
        :rtype: Resource
        """
        raise NotImplemented


class RandomResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def choose_resource(self, student, available_resources):
        """
        :type student: Student
        :type available_resources: tuple[Resource]
        :rtype: Resource
        """
        return random.choice(available_resources)


class RationalResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def choose_resource(self, student, available_resources):
        """
        :type student: Student
        :type available_resources: tuple[Resource]
        :rtype: Resource
        """
        def calculate_absolute_competency_delta(resource):
            return sum(delta for delta in student.calculate_competency_delta(resource.get_competencies(student)).values())

        return max(available_resources, key=calculate_absolute_competency_delta)
