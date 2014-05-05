from agents.behaviors.student.resource_choice import RationalResourceChoiceBehavior, RandomResourceChoiceBehavior
from agents.behaviors.student.knowledge_acquisition import GetAllFactsAcquisitionBehavior

__author__ = 'john'


def _get_all_behaviors():
    return [
        RationalResourceChoiceBehavior,
        RandomResourceChoiceBehavior,

        GetAllFactsAcquisitionBehavior
    ]