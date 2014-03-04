__author__ = 'john'


class StudentSpecification(object):
    def __init__(self, student_name, knowledge, behavior, student_id = None):
        self.student_id = student_id
        """ :type: int """
        self.student_name = student_name
        """ :type: str """
        self.knowledge = knowledge
        """ :type: dict[str, float] """
        self.behavior = behavior
        """ :type: str """
