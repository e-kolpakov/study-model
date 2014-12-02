import random

from agents.student.behaviors.common import GoalDrivenBehaviorMixin
from knowledge_representation import get_available_facts


__author__ = 'e.kolpakov'


class ResourceChoiceMixin:
    def resource_choice_map(self, student, curriculum, available_resources, remaining_time=None):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :return dict[Resource, float]: Resource to confidence map
        """
        raise NotImplemented

    def choose_resource(self, student, curriculum, available_resources, remaining_time=None):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :return Resource: Chosen resource
        """
        resource_choices = self.resource_choice_map(student, curriculum, available_resources, remaining_time)
        return max(resource_choices, key=resource_choices.get)


class BaseResourceChoiceBehavior(ResourceChoiceMixin):
    pass


class RandomResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def resource_choice_map(self, student, curriculum, available_resources, remaining_time=None):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :return dict[Resource, float]: Resource to confidence map
        """
        return {resource: random.random() for resource in available_resources}


class RationalResourceChoiceBehavior(BaseResourceChoiceBehavior):
    def resource_choice_map(self, student, curriculum, available_resources, remaining_time=None):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: tuple[Resource]
        :return dict[Resource, float]: Resource to confidence map
        """
        def new_facts_count(resource):
            facts = set(resource.facts_to_study)
            available_facts = get_available_facts(facts, student.knowledge)
            return len(available_facts)

        return {resource: new_facts_count(resource) for resource in available_resources}


class GoalDrivenResourceChoiceBehavior(BaseResourceChoiceBehavior, GoalDrivenBehaviorMixin):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super(GoalDrivenResourceChoiceBehavior, self).__init__(*args, **kwargs)

    def call_handler_method(self, handler, *args, **kwargs):
        return handler.resource_choice_map(*args, **kwargs)

    def resource_choice_map(self, student, curriculum, available_resources, remaining_time=None):
        return self.get_behavior_result(
            student.goals, ResourceChoiceMixin,
            student, curriculum, available_resources, remaining_time
        )
