from abc import ABC, abstractmethod

from agents.student.activities import StudySessionActivity

from agents.student.behaviors.resource_choice import ResourceChoiceMixin
from agents.student.behaviors.stop_participation import StopParticipationBehaviorMixin
from knowledge_representation import get_available_facts


__author__ = 'e.kolpakov'


class AbstractGoal(ABC, StopParticipationBehaviorMixin):
    def __init__(self, weight=1.0):
        self.weight = weight

    @abstractmethod
    def achieved(self, student):
        pass

    def stop_participation(self, student, curriculum, available_resources):
        return self.achieved(student)

    def requires_activity(self, student, activity_type):
        return True


class WeightedFactGoalMixin:
    TARGET_FACT_WEIGHT = 1.0
    DEPENDENCY_FACT_WEIGHT = 0.5
    OTHER_FACT_WEIGHT = 0.1

    def __init__(self, target_facts=None, *args, **kwargs):
        self.target_facts_codes = frozenset(fact.code for fact in target_facts)
        self.dependency_codes = frozenset(dep_code for fact in target_facts for dep_code in fact.dependencies)
        super(WeightedFactGoalMixin, self).__init__(*args, **kwargs)

    def _get_fact_weight(self, fact):
        result = 0
        if fact.code in self.target_facts_codes:
            result += self.TARGET_FACT_WEIGHT
        if fact.code in self.dependency_codes:
            result += self.DEPENDENCY_FACT_WEIGHT
        return result if result > 0 else self.OTHER_FACT_WEIGHT

    def get_resource_facts_weight(self, resource, prior_knowledge):
        facts = set(resource.facts_to_study)
        available_facts = get_available_facts(facts, prior_knowledge)
        return sum(map(self._get_fact_weight, available_facts))

    # Still uses greedy approach. A* suits better, but a bit more complicated, so requires more thorough testing
    # TODO implement using A* or other efficient graph search algorithm
    # TODO add unit tests
    def resource_choice_map(self, student, curriculum, available_resources, remaining_time=None):
        return {resource: self.get_resource_facts_weight(resource, student.knowledge) for resource in available_resources}


class StudyCompetenciesGoal(WeightedFactGoalMixin, ResourceChoiceMixin, AbstractGoal):
    TARGET_FACT_WEIGHT = 1.0
    DEPENDENCY_FACT_WEIGHT = 0.5
    OTHER_FACT_WEIGHT = 0.1

    def __init__(self, target_competencies, **kwargs):
        self._target_competencies = target_competencies
        target_facts = frozenset(fact for competency in target_competencies for fact in competency.facts)
        super(StudyCompetenciesGoal, self).__init__(target_facts=target_facts, **kwargs)

    def achieved(self, student):
        return all(competency.is_mastered(student.knowledge) for competency in self._target_competencies)

    def requires_activity(self, student, activity_type):
        if activity_type == StudySessionActivity and self.achieved(student):
            return False
        return super().requires_activity(student, activity_type)


class StudyAllCompetenciesGoal(StudyCompetenciesGoal):
    def __init__(self, curriculum, **kwargs):
        target_competencies = curriculum.all_competencies()
        super(StudyAllCompetenciesGoal, self).__init__(target_competencies)

    def achieved(self, student):
        return all(competency.is_mastered(student.knowledge) for competency in self._target_competencies)

    def requires_activity(self, student, activity_type):
        if activity_type == StudySessionActivity and self.achieved(student):
            return False
        return super().requires_activity(student, activity_type)


class PassExamGoal(WeightedFactGoalMixin, ResourceChoiceMixin, AbstractGoal):
    TARGET_FACT_WEIGHT = 0.5
    DEPENDENCY_FACT_WEIGHT = 0.3
    OTHER_FACT_WEIGHT = 0.0

    def __init__(self, target_exam, **kwargs):
        self._target_exam = target_exam
        super(PassExamGoal, self).__init__(target_facts=self._target_exam.facts, **kwargs)

    def achieved(self, student):
        exam_results = student.exam_results.get(self._target_exam.code, [])
        return any(result.passed for result in exam_results)

    def requires_activity(self, student, activity_type):
        if activity_type == StudySessionActivity and self.achieved(student):
            return False
        return super().requires_activity(student, activity_type)
