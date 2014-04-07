import random
from agents.behaviors.base_behavior import BaseBehavior
from utils.calculations import get_competency_delta

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
            return sum(
                delta for delta
                in self._calculate_competency_delta(student, resource.get_competencies(student)).values()
            )

        return max(available_resources, key=calculate_absolute_competency_delta)

    @staticmethod
    def _calculate_competency_delta(student, competencies):
        """
        :type student: Student
        :type competencies: dict[Competency, double]
        :rtype: dict[str, double]
        """
        estimated_competency = {
            competency: value * competency.get_value_multiplier(student)
            for competency, value in competencies.items()
        }
        return get_competency_delta(estimated_competency, student.competencies)
