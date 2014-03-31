__author__ = 'john'


class SimulationInput:
    def __init__(self):
        self._students = []
        self._resources = []
        self._competencies = []

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
    def competencies(self):
        """
        :rtype: list[str]
        """
        return self._competencies

    def _assign_default_competencies(self):
        for student in self.students:
            student.competencies.update(
                {competency: 0 for competency in self.competencies if competency not in student.competencies}
            )

    def prepare(self):
        self._assign_default_competencies()

