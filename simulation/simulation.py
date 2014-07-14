from simulation.resource_lookup_service import ResourceLookupService
from simpy import Environment


__author__ = 'e.kolpakov'


def stop_condition(simulation_state):
    """
    :type simulation_state: SimulationState
    :rtype: bool
    """
    return all(
        competency.is_mastered(student.knowledge)
        for student in simulation_state.students
        for competency in simulation_state.curriculum.all_competencies())


class Simulation(ResourceLookupService):
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
        for student in self._students:
            student.resource_lookup_service = self
            student.curriculum = self._curriculum
            student.env = self._environment
            self._environment.process(student.study())
            student_stop_conditions.append(student.stop_participation_event)

        self._grant_initial_access_permissions()

        self._environment.run(self._environment.all_of(student_stop_conditions))


class SimulationState():
    def __init__(self, students, resources, curriculum):
        """
        :type students: tuple[agents.Student] | list[agents.Student]
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


class SimulationResult():
    def __init__(self):
        super(SimulationResult, self).__init__()

    def resource_usage_listener(self, agent, step_number, args, kwargs):
        """
        :param agent: BaseAgent
        :param step_number: int
        :param args: list[Any]
        :param kwargs: dict[str, Any]
        :return:
        """
        pass

    def knowledge_snapshot_listener(self, agent, step_number, value):
        """
        :type agent: BaseAgent
        :type step_number: int
        :type value:
        """
        pass

    def knowledge_delta_listener(self, agent, step_number, delta):
        """
        :type agent: BaseAgent
        :type delta:
        :type step_number: int
        """
        pass


class Parameters:
    RESOURCE_USAGE = 'Resource.Usage'
    KNOWLEDGE_SNAPSHOT = 'Knowledge.Snapshot'
    KNOWLEDGE_DELTA = 'Knowledge.Delta'