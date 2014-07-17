from collections import defaultdict
from infrastructure.observers import Observer, DeltaObserver, AgentCallObserver

import logging
from simulation.simulation import Parameters

__author__ = 'e.kolpakov'


class BaseAgent:

    agent_count_by_type = defaultdict(int)

    def __init__(self, agent_id=None):
        actual_type = type(self)
        self.agent_count_by_type[actual_type] += 1
        self._agent_id = agent_id if agent_id else actual_type.__name__ + str(self.agent_count_by_type[actual_type])
        self._env = None

    @property
    def agent_id(self):
        return self._agent_id

    @property
    def env(self):
        """
        :rtype: simpy.Environment
        """
        return self._env

    @env.setter
    def env(self, value):
        """
        :param value: simpy.Environment
        """
        self._env = value


class Resource(BaseAgent):
    def __init__(self, name, resource_facts, behavior=None, *args, **kwargs):
        """
        :type name: str
        :type resource_facts: list[knowledge_representation.ResourceFact]
        """
        super(Resource, self).__init__(*args, **kwargs)
        self._name = name
        self._behavior = behavior
        self._facts = resource_facts

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @property
    def facts(self):
        """
        :rtype: tuple[knowledge_representation.ResourceFact]
        """
        return tuple(self._facts)


class IntelligentAgent(BaseAgent):
    pass


class Student(IntelligentAgent):
    def __init__(self, name, knowledge, behavior, *args, **kwargs):
        """
        :type knowledge: list[knowledge_representation.Fact]
        :type behavior: BehaviorGroup
        """
        super(Student, self).__init__(*args, **kwargs)
        self._name = name
        self._behavior = behavior
        self._knowledge = set(knowledge)
        self._curriculum = None
        self._resource_lookup_service = None

        self._stop_participation_event = None

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
        :rtype: knowledge_representation.Curriculum
        """
        return self._curriculum

    @curriculum.setter
    def curriculum(self, value):
        """
        :type value: knowledge_representation.Curriculum
        """
        self._curriculum = value

    @property
    @Observer.observe(topic=Parameters.KNOWLEDGE_SNAPSHOT)
    @DeltaObserver.observe(topic=Parameters.KNOWLEDGE_SNAPSHOT, delta=lambda x, y: x-y)
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
        yield self.env.timeout(1)
        if not self._stop_participation(available_resources):
            yield self.env.process(self.study())
        else:
            self.stop_participation_event.succeed()

    @AgentCallObserver.observe(topic=Parameters.RESOURCE_USAGE)
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

    def _stop_participation(self, available_resources):
        """
        :type available_resources: tuple[Resource]
        :rtype: bool
        """
        return self._behavior.stop_participation.stop_participation(self, self.curriculum, available_resources)