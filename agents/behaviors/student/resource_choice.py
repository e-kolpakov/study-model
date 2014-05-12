import logging
import random
from utils.calculations import get_competency_delta, add_competencies

__author__ = 'john'


class BaseResourceChoiceBehavior:
    def __init__(self):
        super().__init__()

    def choose_resource(self, student, curriculum, available_resources):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :rtype: Resource
        """
        raise NotImplemented


class RandomResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def choose_resource(self, student, curriculum, available_resources):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :rtype: Resource
        """
        return random.choice(available_resources)


class RationalResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def choose_resource(self, student, curriculum, available_resources):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :rtype: Resource
        """
        def new_facts_count(resource):
            # TODO: implement competency dependencies
            facts = set([resource_fact.fact for resource_fact in resource.facts])
            return len(facts - student.knowledge)

        return max(available_resources, key=new_facts_count)