from agents.student.behaviors.resource_choice import ResourceChoiceMixin
from knowledge_representation import get_available_facts

__author__ = 'e.kolpakov'


class StudyGoalBase:
    pass


class StudyCompetenciesGoal(ResourceChoiceMixin):
    TARGET_COMPETENCY_FACT_WEIGHT = 1.0
    DEPENDENCY_FACT_WEIGHT = 0.5
    OTHER_FACT_WEIGHT = 0.1

    def __init__(self, target_competencies):
        self._target_competencies = target_competencies

        self._target_facts = frozenset(fact for competency in self._target_competencies for fact in competency.facts)
        all_dependency_codes = frozenset(dep_code for fact in self._target_facts for dep_code in fact.dependencies)
        self._dependency_codes = all_dependency_codes - set(fact.code for fact in self._target_facts)

    def _get_fact_weight(self, fact):
        if fact in self._target_facts:
            return self.TARGET_COMPETENCY_FACT_WEIGHT
        if fact.code in self._dependency_codes:
            return self.DEPENDENCY_FACT_WEIGHT
        return self.OTHER_FACT_WEIGHT

    # Still uses greedy approach. A* suits better, but a bit more complicated, so requires more thorough testing
    # TODO implement using A* or other efficient graph search algorithm
    # TODO add unit tests
    def choose_resource(self, student, curriculum, available_resources, remaining_time=None):
        def weighted_new_facts_count(resource):
            facts = set([resource_fact.fact for resource_fact in resource.facts])
            available_facts = get_available_facts(facts, student.knowledge)
            return sum(map(self._get_fact_weight, available_facts))

        return max(available_resources, key=weighted_new_facts_count)

    def achieved(self, student):
        return all(competency.is_mastered(student.knowledge) for competency in self._target_competencies)

