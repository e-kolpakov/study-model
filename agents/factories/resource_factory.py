from agents.factories.base_factory import BaseFactory
from agents.resource import Resource

from simulation_specification.resource_specification import ResourceSpecification

__author__ = 'john'


class ResourceFactory(BaseFactory):
    def produce(self, product_spec, all_competencies=None):
        """
        :type product_spec: ResourceSpecification
        """
        all_comp = all_competencies if all_competencies else []
        resource = Resource(product_spec.resource_name, product_spec.provides_knowledge,
                            agent_id=product_spec.agent_id,
                            behavior=product_spec.behavior)
        resource.competencies.update(
            {competency: 0 for competency in all_comp if competency not in resource.competencies})
        return resource