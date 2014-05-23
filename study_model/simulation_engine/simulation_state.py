__author__ = 'e.kolpakov'


class SimulationState:
    def __init__(self, students, resources, curriculum):
        """
        :type students: tuple[Student]
        :type resources: tuple[Resource]
        :type curriculum: Curriculum
        """
        self._step = 0
        self._students = students
        self._resources = resources
        self._curriculum = curriculum

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
    def curriculum(self):
        """
        :rtype: Curriculum
        """
        return self._curriculum