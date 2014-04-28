__author__ = 'john'


class BaseKnowledgeAcquisitionBehavior:
    def __init__(self):
        super().__init__()

    def acquire_facts(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        :rtype: set[Fact]
        """
        raise NotImplemented


class AllPrerequisitesRequiredKnowledgeAcquisitionBehavior(BaseKnowledgeAcquisitionBehavior):
    def acquire_facts(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        :rtype: set[Fact]
        """
        return set()