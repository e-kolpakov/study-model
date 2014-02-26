__author__ = 'john'

from agents.base_agent import BaseAgent


class Student(BaseAgent):
    def __init__(self, spec):
        """
        :param StudentSpecification spec: Student Specification
        """

        super(Student, self).__init__(agent_id=spec.student_id)
        self._knowledge = spec.knowledge
        self._behavior = spec.behavior

    @property
    def knowledge(self):
        return self._knowledge