from agents.behaviors.student.resource_choise.base import BaseResourceChoiceBehavior

__author__ = 'john'


class RationalResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def choose_resource(self, student, available_resources):
        """
        :type student: Student
        :type available_resources: list[Resource]
        :rtype: Resource
        """
        def calculate_absolute_competency_delta(resource):
            return sum(delta for delta in student.calculate_competency_delta(resource).values())

        return max(available_resources, key=calculate_absolute_competency_delta)

