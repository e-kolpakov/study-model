import logging

from pubsub import pub

from agents.base_agent_with_competencies import BaseAgentWithCompetencies
from agents.resource import Resource
from simulation_engine.topics import Topics
from utils.calculations import get_competency_delta


__author__ = 'john'


class Student(BaseAgentWithCompetencies):
    def __init__(self, name, competencies, behavior, *args, **kwargs):
        """
        :type competencies: dict[str, double]
        :type behavior: BehaviorGroup
        """
        super().__init__(competencies, *args, **kwargs)
        self._name = name
        self._behavior = behavior
        self._resource_lookup_service = None
        self._competency_lookup_service = None

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
    def competency_lookup_service(self):
        """
        :rtype: CompetencyLookupService
        """
        return self._competency_lookup_service

    @competency_lookup_service.setter
    def competency_lookup_service(self, value):
        """
        :type value: CompetencyLookupService
        """
        self._competency_lookup_service = value

    def get_knowledge(self, competencies=None):
        """
        :type competencies: tuple[str]
        """
        comp = competencies if competencies else self.competencies.keys()

        return {competency: self.competencies.get(competency, 0) for competency in comp}

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

    def study_resource(self, resource):
        """
        :type resource: Resource
        :rtype: None
        """
        logger = logging.getLogger(__name__)
        logger.debug("Studying resource")

        logger.debug("Updating self knowledge")
        incoming_competencies = self._acquire_competencies(resource)
        new_competencies = self.get_new_competencies(incoming_competencies)

        logger.debug("Calculating delta")
        competency_delta = get_competency_delta(new_competencies, self.competencies)

        self._competencies.update(new_competencies)

        logger.debug("Sending messages")
        pub.sendMessage(Topics.RESOURCE_USAGE, student=self, resource=resource)
        pub.sendMessage(Topics.KNOWLEDGE_SNAPSHOT, student=self, competencies=self.competencies)
        pub.sendMessage(Topics.KNOWLEDGE_DELTA, student=self, competency_delta=competency_delta)

        logger.debug("Student {name}: Studying resource {resource_name} done".format(
            name=self.name,
            resource_name=resource.name))

    def get_value_multiplier(self, resource, competency_code):
        """
        :type resource: Resource
        :rtype: float
        """
        competency = self.competency_lookup_service.get_competency(competency_code)
        return self._behavior.knowledge_acquisition.calculate_prerequisites_multiplier(
            self, resource, competency
        )

    def get_new_competencies(self, incoming_competencies):
        """
        :type incoming_competencies: dict[str, double]
        """
        return {
            competency_code: min(value + self.competencies.get(competency_code, 0), 1.0)
            for competency_code, value in incoming_competencies.items()
        }

    def _choose_resource(self, available_resources):
        """
        :type available_resources: tuple[Resource]
        :rtype: Resource
        """
        return self._behavior.resource_choice.choose_resource(self, available_resources)

    def _competency_change(self, resource, competency, value):
        return self._competencies.get(competency, 0) + value * resource.get_value_multiplier(self, competency)

    def _acquire_competencies(self, resource):
        """
        :type resource: Resource
        :rtype: dict[str, float]
        """
        return self._behavior.knowledge_acquisition.get_competencies(self, resource)