import logging

from simulation import schedulers
from simulation.observers import Observer, DeltaObserver, AgentCallObserver

from study_model.agents.intelligent_agent import IntelligentAgent
from study_model.mooc_simulation.simulation import Topics


__author__ = 'e.kolpakov'


class Student(IntelligentAgent):
    def __init__(self, name, knowledge, behavior, *args, **kwargs):
        """
        :type knowledge: list[Fact]
        :type behavior: BehaviorGroup
        """
        super(Student, self).__init__(*args, **kwargs)
        self._name = name
        self._behavior = behavior
        self._knowledge = set(knowledge)
        self._curriculum = None
        self._resource_lookup_service = None

    @property
    def name(self):
        return self._name

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
        :rtype: Curriculum
        """
        return self._curriculum

    @curriculum.setter
    def curriculum(self, value):
        """
        :type value: Curriculum
        """
        self._curriculum = value

    @property
    @DeltaObserver.observe(Topics.KNOWLEDGE_DELTA, delta=lambda current, prev: current - prev)
    @Observer.observe(Topics.KNOWLEDGE_SNAPSHOT, converter=len)
    def knowledge(self):
        """
        :rtype: frozenset
        """
        return frozenset(self._knowledge)

    @schedulers.steps()
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

        self.study_resource(resource_to_study)

    @AgentCallObserver.observe(Topics.RESOURCE_USAGE)
    def study_resource(self, resource):
        """
        :type resource: Resource
        :rtype: None
        """
        logger = logging.getLogger(__name__)
        logger.debug("Studying resource")

        logger.debug("Updating self knowledge")
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