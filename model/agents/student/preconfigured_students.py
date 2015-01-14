from .student import Student
from model.agents.student.behaviors.behavior_group import BehaviorGroup
from model.agents.student.behaviors.knowledge_acquisition import AllDependenciesAcquisitionBehavior
from model.agents.student.behaviors.resource_choice import RationalResourceChoiceBehavior, GoalDrivenResourceChoiceBehavior
from model.agents.student.behaviors.stop_participation import (
    CourseCompleteStopParticipationBehavior, AllGoalsAchievedStopParticipationBehavior
)
from model.agents.student.behaviors.student_interaction import (
    RandomFactToAllStudentsInteractionBehavior, RandomFactToRandomStudentsInteractionBehavior
)
from model.agents.student.behaviors.activity_period import QuarterHourRandomActivityLengthsBehavior


__author__ = 'e.kolpakov'


__all__ = ['RandomStudent', 'RationalStudent', 'GoalDrivenStudent']


class RationalStudentBehaviorMixin:
    def get_behavior(self, **kwargs):
        return BehaviorGroup.make_group(
            resource_choice=RationalResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
            send_messages=RandomFactToAllStudentsInteractionBehavior(),
            activity_periods=QuarterHourRandomActivityLengthsBehavior(
                study_period=kwargs.get('study_period', 4),
                idle_period=kwargs.get('idle_period', 18),
                peer_interaction_period=kwargs.get('peer_interaction_period', 2)
            )
        )


class RandomStudentBehaviorMixin:
    def get_behavior(self, **kwargs):
        return BehaviorGroup.make_group(
            resource_choice=RationalResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
            send_messages=RandomFactToRandomStudentsInteractionBehavior(),
            activity_periods=QuarterHourRandomActivityLengthsBehavior(
                study_period=kwargs.get('study_period', 4),
                idle_period=kwargs.get('idle_period', 18),
                peer_interaction_period=kwargs.get('peer_interaction_period', 2)
            )
        )


class GoalDrivenBehaviorMixin:
    def get_behavior(self, **kwargs):
        return BehaviorGroup.make_group(
            resource_choice=GoalDrivenResourceChoiceBehavior(RationalResourceChoiceBehavior()),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=AllGoalsAchievedStopParticipationBehavior(CourseCompleteStopParticipationBehavior()),
            send_messages=RandomFactToRandomStudentsInteractionBehavior(),
            activity_periods=QuarterHourRandomActivityLengthsBehavior(
                study_period=kwargs.get('study_period', 4),
                idle_period=kwargs.get('idle_period', 18),
                peer_interaction_period=kwargs.get('peer_interaction_period', 2)
            )
        )


class RationalStudent(Student, RationalStudentBehaviorMixin):
    def __init__(self, name, knowledge, **kwargs):
        behavior = self.get_behavior(**kwargs)
        super(RationalStudent, self).__init__(name, knowledge, behavior, **kwargs)


class RandomStudent(Student, RandomStudentBehaviorMixin):
    def __init__(self, name, knowledge, **kwargs):
        behavior = self.get_behavior(**kwargs)
        super(RandomStudent, self).__init__(name, knowledge, behavior, **kwargs)


class GoalDrivenStudent(Student, GoalDrivenBehaviorMixin):
    def __init__(self, name, knowledge, **kwargs):
        behavior = self.get_behavior(**kwargs)
        super(GoalDrivenStudent, self).__init__(name, knowledge, behavior, **kwargs)