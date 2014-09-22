import logging

from agents.base_agents import IntelligentAgent
from agents.student.activities import IdleStudentActivity, StudySessionStudentActivity
from agents.student.behaviors.behavior_group import BehaviorGroup
from agents.student.behaviors.knowledge_acquisition import AllDependenciesAcquisitionBehavior
from agents.student.behaviors.resource_choice import RationalResourceChoiceBehavior, RandomResourceChoiceBehavior
from agents.student.behaviors.stop_participation import CourseCompleteStopParticipationBehavior
from agents.student.behaviors.study_period import QuarterHourRandomStudyPeriodBehavior
from infrastructure.descriptors import TypedDescriptor, TypedDescriptorWithDefault
from infrastructure.observers import Observer, DeltaObserver, observer_trigger, AgentCallObserver
from simulation.result import ResultTopics

__author__ = 'e.kolpakov'


class Student(IntelligentAgent):

    idle_activity = TypedDescriptorWithDefault(IdleStudentActivity, 'idle_activity')
    study_session_activity = TypedDescriptorWithDefault(StudySessionStudentActivity, 'study_session_activity')

    def __init__(self, name, knowledge, behavior, skill=None, **kwargs):
        """
        :type name: str
        :type knowledge: list[knowledge_representation.Fact]
        :type behavior: BehaviorGroup
        :type skill: double
        """
        super(Student, self).__init__(**kwargs)
        self._name = name
        self._behavior = behavior
        self._knowledge = set(knowledge)
        self._skill = skill if skill else 1

        # injected properties
        self._curriculum = None
        self._resource_lookup_service = None
        self._stop_participation_event = None

        self._logger = logging.getLogger(__name__)

    @property
    def name(self):
        return self._name

    @property
    @Observer.observe(topic=ResultTopics.KNOWLEDGE_SNAPSHOT)
    @Observer.observe(topic=ResultTopics.KNOWLEDGE_COUNT, converter=lambda x: len(x))
    @DeltaObserver.observe(topic=ResultTopics.KNOWLEDGE_DELTA, delta=lambda x, y: x - y)
    def knowledge(self):
        """
        :rtype: frozenset
        """
        return frozenset(self._knowledge)

    @property
    def stop_participation_event(self):
        if not self._stop_participation_event:
            self._stop_participation_event = self.env.event()
        return self._stop_participation_event

    @property
    def skill(self):
        """ :return: double """
        return self._skill

    @property
    def resource_lookup_service(self):
        """
        :rtype: ResourceLookupService
        """
        return self._resource_lookup_service

    @resource_lookup_service.setter
    def resource_lookup_service(self, value):
        """
        :type value: ResourceLookupService
        """
        self._resource_lookup_service = value

    @property
    def curriculum(self):
        """
        :rtype: knowledge_representation.Curriculum
        """
        return self._curriculum

    @curriculum.setter
    def curriculum(self, value):
        """
        :type value: knowledge_representation.Curriculum
        """
        self._curriculum = value

    def study(self):
        while not self.stop_participation_event.processed:
            study_session_length = self._behavior.study_period.get_study_period(self, self.env.now)
            yield self.env.process(self.study_session_activity.activate(
                self, study_session_length,
                get_resources_callback=lambda: self.resource_lookup_service.get_accessible_resources(self),
                choose_resource_callback=lambda res: self._choose_resource(res)
            ))

            idle_session_length = self._behavior.study_period.get_idle_period(self, self.env.now)
            yield self.env.process(self.idle_activity.activate(self, idle_session_length))

    @observer_trigger
    @AgentCallObserver.observe(topic=ResultTopics.RESOURCE_USAGE)
    def study_resource(self, resource):
        """
        :type resource: Resource
        :rtype: None
        """
        self._logger.debug("Updating knowledge")
        knowledge_to_acquire = self._acquire_knowledge(resource)
        time_to_study = self._get_time_to_study(knowledge_to_acquire)
        yield self.env.timeout(time_to_study)
        self._add_knowledge(knowledge_to_acquire)

        self._logger.debug("Student {name}: Studying resource {resource_name} done at {time}".format(
            name=self.name, resource_name=resource.name, time=self.env.now
        ))
        return

    @observer_trigger
    def _add_knowledge(self, new_knowledge):
        self._knowledge = self._knowledge | new_knowledge

    def _get_time_to_study(self, facts):
        """
        Calculates time required to study a set of facts
        :param facts: frozenset[knowledge_representation.Fact]
        :return: double
        """
        return sum(fact.complexity for fact in facts) / self.skill

    def _choose_resource(self, available_resources):
        """
        :type available_resources: tuple[Resource]
        :rtype: Resource
        """
        return self._behavior.resource_choice.choose_resource(self, self.curriculum, available_resources)

    def _acquire_knowledge(self, resource):
        """
        :type resource: Resource
        :rtype: frozenset[knowledge_representation.Fact]
        """
        return self._behavior.knowledge_acquisition.acquire_facts(self, resource)

    def check_stop_participation(self, available_resources):
        """
        :type available_resources: tuple[Resource]
        :rtype: bool
        """
        should_stop = self._behavior.stop_participation.stop_participation(self, self.curriculum, available_resources)
        if should_stop:
            self.stop_participation_event.succeed()
        return should_stop


class RationalStudent(Student):
    def __init__(self, name, knowledge, **kwargs):
        behavior = BehaviorGroup.make_group(
            resource_choice=RationalResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
            study_period=QuarterHourRandomStudyPeriodBehavior(kwargs.get('study_period', 10), kwargs.get('idle_period', 20))
        )
        super(RationalStudent, self).__init__(name, knowledge, behavior, **kwargs)


class RandomStudent(Student):
    def __init__(self, name, knowledge, **kwargs):
        behavior = BehaviorGroup.make_group(
            resource_choice=RandomResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
            study_period=QuarterHourRandomStudyPeriodBehavior(kwargs.get('study_period', 10), kwargs.get('idle_period', 20))
        )
        super(RandomStudent, self).__init__(name, knowledge, behavior, **kwargs)
