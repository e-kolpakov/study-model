__author__ = 'john'


class StudentSpecification(object):
    def __init__(self, student_name, competencies, behavior, agent_id=None):
        """
        :type agent_id: str | int
        :type student_name: str
        :type competencies: dict[str, float]
        :type behavior: dict[str, str]
        """
        self.agent_id = agent_id
        self.student_name = student_name
        self.competencies = competencies
        self.behavior = behavior
