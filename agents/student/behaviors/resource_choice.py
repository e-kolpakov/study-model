import random
from agents.student.behaviors.common import GoalDrivenBehaviorMixin

from knowledge_representation import get_available_facts


__author__ = 'e.kolpakov'


class ResourceChoiceMixin:
    def choose_resource(self, student, curriculum, available_resources, remaining_time=None):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :rtype: Resource
        """
        raise NotImplemented


class BaseResourceChoiceBehavior(ResourceChoiceMixin):
    pass


class RandomResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def choose_resource(self, student, curriculum, available_resources, remaining_time=None):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :rtype: Resource
        """
        return random.choice(available_resources)


class RationalResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def choose_resource(self, student, curriculum, available_resources, remaining_time=None):
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


class GoalDrivenResourceChoiceBehavior(BaseResourceChoiceBehavior, GoalDrivenBehaviorMixin):
    def __init__(self, *args, **kwargs):
        super(GoalDrivenResourceChoiceBehavior, self).__init__(*args, **kwargs)

    def choose_resource(self, student, curriculum, available_resources, remaining_time=None):
        handler = self.find_goal_handler(student, ResourceChoiceMixin)
        return handler.choose_resource(student, curriculum, available_resources, remaining_time)
