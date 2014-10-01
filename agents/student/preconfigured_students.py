from agents.student import Student
from agents.student.behaviors.behavior_group import BehaviorGroup
from agents.student.behaviors.knowledge_acquisition import AllDependenciesAcquisitionBehavior
from agents.student.behaviors.resource_choice import RationalResourceChoiceBehavior, RandomResourceChoiceBehavior
from agents.student.behaviors.stop_participation import CourseCompleteStopParticipationBehavior
from agents.student.behaviors.study_period import QuarterHourRandomActivityLengthsBehavior

__author__ = 'e.kolpakov'

class RationalStudent(Student):
    def __init__(self, name, knowledge, **kwargs):
        behavior = BehaviorGroup.make_group(
            resource_choice=RationalResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
            activity_periods=QuarterHourRandomActivityLengthsBehavior(
                kwargs.get('activity_periods', 10), kwargs.get('idle_period', 20), kwargs.get('handshake_period', 20)
            )
        )
        super(RationalStudent, self).__init__(name, knowledge, behavior, **kwargs)


class RandomStudent(Student):
    def __init__(self, name, knowledge, **kwargs):
        behavior = BehaviorGroup.make_group(
            resource_choice=RandomResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
            activity_periods=QuarterHourRandomActivityLengthsBehavior(
                kwargs.get('activity_periods', 10), kwargs.get('idle_period', 20), kwargs.get('handshake_period', 20)
            )
        )
        super(RandomStudent, self).__init__(name, knowledge, behavior, **kwargs)