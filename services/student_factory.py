from agents.student import Student

__author__ = 'john'


class StudentFactory(object):
    def __init__(self):
        pass

    def create_student(self, student_spec, competencies=None):
        """
        :param StudentSpecification student_spec: Student specification
        :param list[str] competencies: Optional. List of competencies in the course
        """
        student = Student(student_spec)
        student.knowledge.update({competency: 0 for competency in competencies if competency not in student.knowledge})
        return student