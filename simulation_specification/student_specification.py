__author__ = 'john'


class StudentSpecification(object):
    def __init__(self, student_name, knowledge, behavior, student_id = None):
        self.student_id = student_id
        self.student_name = student_name
        self.knowledge = knowledge
        self.behavior = behavior

