from agents.behaviors.base_behavior import BaseBehavior

__author__ = 'john'


class BaseKnowledgeAcquisitionBehavior(BaseBehavior):
    def __init__(self):
        super().__init__()

    def get_competencies(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        :rtype: dict[str, float]
        """
        raise NotImplemented

    def calculate_prerequisites_multiplier(self, student, resource, prerequisites):
        """
        :type student: Student
        :type resource: Resource
        :type prerequisites: tuple[str]
        :rtype: float
        """
        raise NotImplemented


class AllPrerequisitesRequiredKnowledgeAcquisitionBehavior(BaseKnowledgeAcquisitionBehavior):
    def get_competencies(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        :rtype: dict[str, float]
        """
        competency_lookup = student.competency_lookup_service
        new_competencies = {
            code: value * self.calculate_prerequisites_multiplier(
                student, resource, competency_lookup.get_competency(code).dependencies
            )
            for code, value in resource.competencies.items()
        }
        return new_competencies

    def calculate_prerequisites_multiplier(self, student, resource, prerequisites):
        """
        :type student: Student
        :type resource: Resource
        :type prerequisites: tuple[str]
        :rtype: float
        """
        if not prerequisites:
            return 1
        student_comps = student.get_knowledge(prerequisites)
        resource_comps = {dep: resource.competencies.get(dep, 0) for dep in prerequisites}
        merged_comps = dict()
        for comp in list(student_comps.keys()) + list(resource_comps.keys()):
            merged_comps[comp] = min(student_comps.get(comp, 0) + resource_comps.get(comp, 0), 1.0)
        return 1 if all(value >= 1 for competency, value in merged_comps.items()) else 0