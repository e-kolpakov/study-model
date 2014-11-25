from knowledge_representation import get_available_facts

__author__ = 'e.kolpakov'


class BaseFactsAcquisitionBehavior:
    def acquire_facts(self, student, lecture):
        """
        :type student: Student
        :type resource: Lecture
        :rtype: frozenset[knowledge_representation.Fact]
        """
        raise NotImplemented


class GetAllFactsAcquisitionBehavior(BaseFactsAcquisitionBehavior):
    def acquire_facts(self, student, lecture):
        """
        :type student: agents.student.Student
        :type resource: Lecture
        :rtype: frozenset[knowledge_representation.Fact]
        """
        return frozenset(lecture.facts)


class AllDependenciesAcquisitionBehavior(BaseFactsAcquisitionBehavior):
    def acquire_facts(self, student, lecture):
        """
        :type student: Student
        :type resource: Lecture
        :rtype: frozenset[knowledge_representation.Fact]
        """
        return get_available_facts(lecture.facts, student.knowledge)