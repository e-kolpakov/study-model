from agents.behaviors.student.resource_choice import RationalResourceChoiceBehavior, RandomResourceChoiceBehavior

__author__ = 'john'


def _get_all_behaviors():
    return [RationalResourceChoiceBehavior, RandomResourceChoiceBehavior]