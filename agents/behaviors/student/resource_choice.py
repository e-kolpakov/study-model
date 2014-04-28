import logging
import random
from utils.calculations import get_competency_delta, add_competencies

__author__ = 'john'


class BaseResourceChoiceBehavior:
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
        def new_facts_count(resource):
            return sum(
                delta for delta
                in self._calculate_competency_delta(student, resource).values()
            )

        return max(available_resources, key=new_facts_count)