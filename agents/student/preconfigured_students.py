from agents.student import Student
from agents.student.behaviors.behavior_group import BehaviorGroup
from agents.student.behaviors.knowledge_acquisition import AllDependenciesAcquisitionBehavior
from agents.student.behaviors.resource_choice import RationalResourceChoiceBehavior, RandomResourceChoiceBehavior
from agents.student.behaviors.stop_participation import CourseCompleteStopParticipationBehavior
from agents.student.behaviors.student_interaction import RandomFactToAllStudentsInteractionBehavior, \
    RandomFactToRandomStudentsInteractionBehavior
from agents.student.behaviors.study_period import QuarterHourRandomActivityLengthsBehavior


__author__ = 'e.kolpakov'


class RationalStudentBehaviorMixin:
    def get_brehavior(self, **kwargs):
        return BehaviorGroup.make_group(
            resource_choice=RationalResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
            send_messages=RandomFactToAllStudentsInteractionBehavior(),
            activity_periods=QuarterHourRandomActivityLengthsBehavior(
                kwargs.get('activity_periods', 10), kwargs.get('idle_period', 20), kwargs.get('handshake_period', 20)
            )
        )


class RandomStudentBehaviorMixin:
    def get_brehavior(self, **kwargs):
        return BehaviorGroup.make_group(
            resource_choice=RationalResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
            send_messages=RandomFactToRandomStudentsInteractionBehavior(),
            activity_periods=QuarterHourRandomActivityLengthsBehavior(
                kwargs.get('activity_periods', 10), kwargs.get('idle_period', 20), kwargs.get('handshake_period', 20)
            )
        )


class RationalStudent(Student, RationalStudentBehaviorMixin):
    def __init__(self, name, knowledge, **kwargs):
        behavior = self.get_brehavior(**kwargs)
        super(RationalStudent, self).__init__(name, knowledge, behavior, **kwargs)


class RandomStudent(Student, RandomStudentBehaviorMixin):
    def __init__(self, name, knowledge, **kwargs):
        behavior = self.get_brehavior(**kwargs)
        super(RandomStudent, self).__init__(name, knowledge, behavior, **kwargs)