from agents.student import Student

__author__ = 'john'


class StudentFactory(object):
    def __init__(self):
        pass

    def produce(self, student_spec, all_competencies=None):
        """
        :param StudentSpecification student_spec: Student specification
        """
        all_comp = all_competencies if all_competencies else []
        behavior_group = student_spec.behavior
        student = Student(student_spec.student_name, student_spec.competencies,
                          agent_id=student_spec.agent_id, behavior=behavior_group)
        student.competencies.update(
            {competency: 0 for competency in all_comp if competency not in student.competencies})
        return student
