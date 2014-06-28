from knowledge_representation import get_available_facts

__author__ = 'e.kolpakov'


class BaseFactsAcquisitionBehavior:
    def __init__(self):
        super().__init__()

    def acquire_facts(self, student, resource):
        """
        :type student: agents.Student
        :type resource: Resource
        :rtype: set[knowledge_representation.Fact]
        """
        raise NotImplemented


class GetAllFactsAcquisitionBehavior(BaseFactsAcquisitionBehavior):
    def acquire_facts(self, student, resource):
        """
        :type student: agents.Student
        :type resource: Resource
        :rtype: set[knowledge_representation.Fact]
        """
        return set(resource_fact.fact for resource_fact in resource.facts)


class AllDependenciesAcquisitionBehavior(BaseFactsAcquisitionBehavior):
    def acquire_facts(self, student, resource):
        """
        :type student: agents.Student
        :type resource: Resource
        :rtype: set[knowledge_representation.Fact]
        """
        facts = set(resource_fact.fact for resource_fact in resource.facts)
        return get_available_facts(facts, student.knowledge)