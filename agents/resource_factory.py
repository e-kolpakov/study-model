from agents.base_factory import BaseFactory
from agents.resource import Resource

from simulation_specification.resource_specification import ResourceSpecification

__author__ = 'john'


class ResourceFactory(BaseFactory):
    def __init__(self, competencies=None):
        """
        :param list[str] competencies: Optional. List of competencies in the course
        """
        self._course_competencies = competencies

    def produce(self, product_spec):
        """
        :type product_spec: ResourceSpecification
        """
        resource = Resource(product_spec.resource_name, product_spec.provides_knowledge,
                            agent_id=product_spec.agent_id,
                            behavior=product_spec.behavior)
        resource.competencies.update(
            {competency: 0 for competency in self._course_competencies if competency not in resource.competencies})
        return resource