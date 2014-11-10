from agents.student.behaviors.common import GoalDrivenBehaviorMixin

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

    def stop_participation(self, student, curriculum, available_resources):
        return all(goal.achieved(student) for goal in student.goals)
