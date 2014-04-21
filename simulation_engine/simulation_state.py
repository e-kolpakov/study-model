__author__ = 'john'


class SimulationState(object):
    def __init__(self, students, resources, competencies):
        """
        :type students: tuple[Student]
        :type resources: tuple[Resource]
        :type competencies: tuple[Competency]
        """
        self._step = 0
        self._students = students
        self._resources = resources
        self._competencies = competencies

    @property
    def step(self):
        return self._step

    @property
    def students(self):
        """
        :rtype: tuple(Student)
        """
        return self._students

    @property
    def resources(self):
        """
        :rtype: tuple[Resource]
        """
        return self._resources

    @property
    def competencies(self):
        """
        :rtype: tuple[Competency]
        """
        return self._competencies