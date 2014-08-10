import random

from knowledge_representation import get_available_facts


__author__ = 'e.kolpakov'


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
            facts = set([resource_fact.fact for resource_fact in resource.facts])
            available_facts = get_available_facts(facts, student.knowledge)
            return len(available_facts)

        return max(available_resources, key=new_facts_count)