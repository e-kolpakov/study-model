import logging

from .base_agents import IntelligentAgent
from .behaviors.student.behavior_group import BehaviorGroup
from .behaviors.student.knowledge_acquisition import AllDependenciesAcquisitionBehavior
from .behaviors.student.resource_choice import RationalResourceChoiceBehavior, RandomResourceChoiceBehavior
from .behaviors.student.stop_participation import CourseCompleteStopParticipationBehavior
from infrastructure.observers import Observer, DeltaObserver, observer_trigger, AgentCallObserver
from simulation.result import ResultTopics

__author__ = 'e.kolpakov'


class Student(IntelligentAgent):
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
        self._skill = skill if skill else 0

        # injected properties
        self._curriculum = None
        self._resource_lookup_service = None
        self._stop_participation_event = None

    @property
    def name(self):
        return self._name

    @property
    @Observer.observe(topic=ResultTopics.KNOWLEDGE_SNAPSHOT)
    @DeltaObserver.observe(topic=ResultTopics.KNOWLEDGE_DELTA, delta=lambda x, y: x - y)
    def knowledge(self):
        """
        :rtype: frozenset
        """
        return frozenset(self._knowledge)

    @property
    def resource_lookup_service(self):
        """
        :rtype: ResourceLookupService
        """
        return self._resource_lookup_service

    @property
    def stop_participation_event(self):
        if not self._stop_participation_event:
            self._stop_participation_event = self.env.event()
        return self._stop_participation_event

    @property
    def skill(self):
        """ :return: double """
        return self._skill

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
        logger = logging.getLogger(__name__)
        logger.debug("Student {name} study".format(name=self.name))
        available_resources = self.resource_lookup_service.get_accessible_resources(self)
        if not available_resources:
            logger.warn("No resources available")
            return

        logger.debug("Choosing a resource to study")
        resource_to_study = self._choose_resource(available_resources)
        logger.info("Student {name}({id}): resource {resource_name}({resource_id}) chosen ".format(
            name=self.name, id=self.agent_id,
            resource_name=resource_to_study.name, resource_id=resource_to_study.agent_id
        ))

        yield self.env.timeout(1)
        self.study_resource(resource_to_study)
        if not self._stop_participation(available_resources):
            yield self.env.process(self.study())
        else:
            self.stop_participation_event.succeed()

    @observer_trigger
    @AgentCallObserver.observe(topic=ResultTopics.RESOURCE_USAGE)
    def study_resource(self, resource):
        """
        :type resource: Resource
        :rtype: None
        """
        logger = logging.getLogger(__name__)
        logger.debug("Studying resource")

        logger.debug("Updating knowledge")
        self._knowledge = self._knowledge | self._acquire_knowledge(resource)

        logger.debug("Student {name}: Studying resource {resource_name} done".format(
            name=self.name,
            resource_name=resource.name))

    def _choose_resource(self, available_resources):
        """
        :type available_resources: tuple[Resource]
        :rtype: Resource
        """
        return self._behavior.resource_choice.choose_resource(self, self.curriculum, available_resources)

    def _acquire_knowledge(self, resource):
        """
        :type resource: Resource
        :rtype: dict[str, float]
        """
        return self._behavior.knowledge_acquisition.acquire_facts(self, resource)

    def _stop_participation(self, available_resources):
        """
        :type available_resources: tuple[Resource]
        :rtype: bool
        """
        return self._behavior.stop_participation.stop_participation(self, self.curriculum, available_resources)


class RationalStudent(Student):
    def __init__(self, name, knowledge, **kwargs):
        behavior = BehaviorGroup.make_group(
            resource_choice=RationalResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
        )
        super(RationalStudent, self).__init__(name, knowledge, behavior, **kwargs)


class RandomStudent(Student):
    def __init__(self, name, knowledge, **kwargs):
        behavior = BehaviorGroup.make_group(
            resource_choice=RandomResourceChoiceBehavior(),
            knowledge_acquisition=AllDependenciesAcquisitionBehavior(),
            stop_participation=CourseCompleteStopParticipationBehavior(),
        )
        super(RandomStudent, self).__init__(name, knowledge, behavior, **kwargs)