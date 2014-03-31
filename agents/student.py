import copy
import logging
from random import randint

from pubsub import pub

from agents.base_agent_with_competencies import BaseAgentWithCompetencies
from agents.resource import Resource
from topics import Topics


__author__ = 'john'


class Student(BaseAgentWithCompetencies):
    def __init__(self, name, competencies, behavior, *args, **kwargs):
        """
        :type competencies: dict[Competency, double]
        :type behavior: BehaviorGroup
        """
        super().__init__(competencies, *args, **kwargs)
        self._name = name
        self._behavior = behavior
        self._resource_lookup_service = None

    def get_knowledge(self, competencies=None):
        eff_competencies = competencies if competencies else self.competencies.keys()

        return {competency: self.competencies.get(competency, 0) for competency in eff_competencies}

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

        self._study_resource(resource_to_study)

    def calculate_competency_delta(self, competencies):
        """
        :type competencies: dict[str, double]
        :rtype: dict[str, double]
        """
        return {
            competency: max(value - self.competencies.get(competency, 0), 0)
            for competency, value in competencies.items()
        }

    def _choose_resource(self, available_resources):
        """
        :type available_resources: tuple[Resource]
        :rtype: Resource
        """
        return self._behavior.resource_choice.choose_resource(self, available_resources)

    def _study_resource(self, resource_to_study):
        """
        :type resource_to_study: Resource
        :rtype: None
        """
        logger = logging.getLogger(__name__)
        logger.debug("Studying resource")

        old_knowledge = copy.deepcopy(self.competencies)
        logger.debug("Extracting resource competencies")
        competencies = resource_to_study.get_competencies(self)

        logger.debug("Updating self knowledge")
        for competency, value in competencies.items():
            self._competencies[competency] = min(self._competencies.get(competency, 0) + value, 1.0)

        logger.debug("Calculating delta")
        knowledge_delta = {
            competency: value - old_knowledge.get(competency, 0)
            for competency, value in self.competencies.items()
        }

        logger.debug("Sending messages")
        pub.sendMessage(Topics.RESOURCE_USAGE, student=self, resource=resource_to_study)
        pub.sendMessage(Topics.KNOWLEDGE_SNAPSHOT, student=self, knowledge=self.competencies)
        pub.sendMessage(Topics.KNOWLEDGE_DELTA, student=self, knowledge_delta=knowledge_delta)

        logger.debug("Student {name}: Studying resource {resource_name} done".format(
            name=self.name,
            resource_name=resource_to_study.name))



