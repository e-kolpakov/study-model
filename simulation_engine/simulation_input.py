__author__ = 'e.kolpakov'


class SimulationInput:
    def __init__(self):
        self._students = []
        self._resources = []
        self._competencies = []
        self._curriculum = None

    @property
    def students(self):
        """
        :rtype: list[Student]
        """
        return self._students

    @property
    def resources(self):
        """
        :rtype: list[Resource]
        """
        return self._resources

    @property
    def curriculum(self):
        """
        :rtype: Curriculum
        """
        return self._curriculum

    @curriculum.setter
    def curriculum(self, value):
        """
        :type value: Curriculum
        """
        self._curriculum = value
