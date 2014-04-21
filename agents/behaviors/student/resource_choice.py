import logging
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
                in self._calculate_competency_delta(student, resource).values()
            )

        return max(available_resources, key=calculate_absolute_competency_delta)

    @staticmethod
    def _calculate_competency_delta(student, resource):
        """
        :type student: Student
        :type resource: Resource
        :rtype: dict[str, double]
        """
        competencies = resource.competencies
        estimated_competency = {
            competency: value * student.get_value_multiplier(resource, competency)
            for competency, value in competencies.items()
        }
        _logger = logging.getLogger(RationalResourceChoiceBehavior.__name__)
        _logger.debug("Estimated competency delta:\n{0}".format(estimated_competency))
        return get_competency_delta(estimated_competency, student.competencies)
