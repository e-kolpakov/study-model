__author__ = 'john'


class SimulationSpecification(object):
    def __init__(self):
        self._course_competencies = list()
        self._students = list()
        self._resources = list()

    @property
    def course_competencies(self):
        """
        :rtype: list[string]
        """
        return self._course_competencies

    @property
    def students(self):
        """
        :rtype: list[StudentSpecification]
        """
        return self._students

    @property
    def resources(self):
        """
        :rtype: list[ResourceSpecification[
        """
        return self._resources