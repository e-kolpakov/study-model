from agents.student import Student
from simulation_specification.student_specification import StudentSpecification

__author__ = 'john'


class StudentFactory(object):
    def __init__(self, competencies=None):
        """
        :param list[str] competencies: Optional. List of competencies in the course
        """
        self._course_competencies = competencies

    def produce(self, student_spec):
        """
        :param StudentSpecification student_spec: Student specification
        """
        student = Student(student_spec.student_name, student_spec.competencies,
                          agent_id=student_spec.agent_id, behavior=student_spec.behavior)
        student.competencies.update({competency: 0 for competency in self._course_competencies if competency not in student.competencies})
        return student