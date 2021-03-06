from simpy import Environment

from model.simulation.resource_access import ResourceAccessService


__author__ = 'e.kolpakov'


class Simulation(ResourceAccessService):
    def __init__(self, simulation_input, *args, **kwargs):
        """
        :type simulation_input: study_model.simulation.simulation_input.SimulationInput
        """
        super(Simulation, self).__init__(*args, **kwargs)

        self._step = 0
        """ :type: int """

        self._environment = Environment()

        self._students = simulation_input.students
        self._resources = simulation_input.resources
        self._curriculum = simulation_input.curriculum

        self._register_resources(self._resources)

    @property
    def state(self):
        """ :rtype: SimulationState """
        return SimulationState(self._students, self._resources, self._curriculum)

    def _grant_initial_access_permissions(self):
        for student in self._students:
            for resource in self._resources:
                self.grant_access(student, resource)

    def run(self):
        student_stop_conditions = []
        for resource in self._resources:
            resource.resource_access_service = self
            resource.env = self._environment

        for student in self._students:
            student.curriculum = self._curriculum
            student.env = self._environment
            self._environment.process(student.start())
            student_stop_conditions.append(student.stop_participation_event)

        self._grant_initial_access_permissions()

        self._environment.run(self._environment.all_of(student_stop_conditions))


class SimulationState():
    def __init__(self, students, resources, curriculum):
        """
        :type students: tuple[agents.student] | list[agents.student]
        :type resources: tuple[Resource] | list[Resource]
        :type curriculum: knowledge_representation.Curriculum
        """
        super(SimulationState, self).__init__()
        self._students = students
        self._resources = resources
        self._curriculum = curriculum

    @property
    def students(self):
        """ :rtype: tuple(Student) """
        return tuple(self._students)

    @property
    def resources(self):
        """ :rtype: tuple[Resource] """
        return tuple(self._resources)

    @property
    def curriculum(self):
        """ :rtype: knowledge_representation.Curriculum """
        return self._curriculum


