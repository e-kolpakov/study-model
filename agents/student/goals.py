from agents.student.behaviors.resource_choice import ResourceChoiceMixin
from knowledge_representation import get_available_facts

__author__ = 'e.kolpakov'


class StudyGoalBase:
    pass


class StudyCompetenciesGoal(ResourceChoiceMixin):
    def __init__(self, target_competencies):
        self._target_competencies = target_competencies

    def choose_resource(self, student, curriculum, available_resources, remaining_time=None):
        def new_facts_count(resource):
            facts = set([resource_fact.fact for resource_fact in resource.facts])
            available_facts = get_available_facts(facts, student.knowledge)
            return len(available_facts)

        return max(available_resources, key=new_facts_count)

