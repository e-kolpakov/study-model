from model.agents.student.behaviors.common import GoalDrivenBehaviorMixin

__author__ = 'e.kolpakov'


class StopParticipationBehaviorMixin:
    def stop_participation(self, student, curriculum, available_resources):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: list[Resource] | tuple[Resource]
        :rtype: bool
        """
        pass


class BaseStopParticipationBehavior(StopParticipationBehaviorMixin):
    pass


class CourseCompleteStopParticipationBehavior(BaseStopParticipationBehavior):
    def stop_participation(self, student, curriculum, available_resources):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: list[Resource] | tuple[Resource]
        :rtype: bool
        """
        return all(competency.is_mastered(student.knowledge) for competency in curriculum.all_competencies())


class AllGoalsAchievedStopParticipationBehavior(BaseStopParticipationBehavior, GoalDrivenBehaviorMixin):
    def __init__(self, *args, **kwargs):
        super(AllGoalsAchievedStopParticipationBehavior, self).__init__(*args, **kwargs)

    def call_handler_method(self, handler, *args, **kwargs):
        return handler.stop_participation(*args, **kwargs)

    def merge_goal_results(self, results):
        return all(results.values())

    def stop_participation(self, student, curriculum, available_resources):
        return self.get_behavior_result(
            student.goals, StopParticipationBehaviorMixin,
            student, curriculum, available_resources
        )
