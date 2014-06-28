from simulation.step_simulation.simulation import Simulation, SimulationState
from simulation.step_simulation.result import SimulationResult, SimulationResultItem
from mooc_simulation.resource_lookup_service import ResourceLookupService


__author__ = 'e.kolpakov'


def stop_condition(simulation_state):
    """
    :type simulation_state: MoocSimulationState
    :rtype: bool
    """
    return all(
        competency.is_mastered(student.knowledge)
        for student in simulation_state.students
        for competency in simulation_state.curriculum.all_competencies())


class MoocSimulation(ResourceLookupService, Simulation):
    def __init__(self, simulation_input, *args, **kwargs):
        """
        :type simulation_input: study_model.mooc_simulation.simulation_input.SimulationInput
        """
        super(MoocSimulation, self).__init__(*args, **kwargs)

        self._step = 0
        """ :type: int """

        self._students = simulation_input.students
        self._resources = simulation_input.resources
        self._curriculum = simulation_input.curriculum

        self._register_resources(self._resources)

        self._register_agents(self._students)
        self._register_agents(self._resources)

    @property
    def state(self):
        """ :rtype: MoocSimulationState """
        return MoocSimulationState(self._students, self._resources, self._curriculum)

    def _grant_initial_access_permissions(self):
        for student in self._students:
            for resource in self._resources:
                self.grant_access(student, resource)

    def initialize(self):
        for student in self._students:
            student.resource_lookup_service = self
            student.curriculum = self._curriculum

        self._grant_initial_access_permissions()


class MoocSimulationState(SimulationState):
    def __init__(self, students, resources, curriculum):
        """
        :type students: tuple[Student] | list[Student]
        :type resources: tuple[Resource] | list[Resource]
        :type curriculum: Curriculum
        """
        super(MoocSimulationState, self).__init__()
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
        """ :rtype: Curriculum """
        return self._curriculum


class MoocSimulationResult(SimulationResult):
    def __init__(self):
        super(MoocSimulationResult, self).__init__()
        self._register_result_handler(self.resource_usage_listener, Parameters.RESOURCE_USAGE)
        self._register_result_handler(self.knowledge_snapshot_listener, Parameters.KNOWLEDGE_SNAPSHOT)
        self._register_result_handler(self.knowledge_delta_listener, Parameters.KNOWLEDGE_DELTA)

    def resource_usage_listener(self, agent, step_number, args, kwargs):
        """
        :param agent: BaseAgent
        :param step_number: int
        :param args: list[Any]
        :param kwargs: dict[str, Any]
        :return:
        """
        result = SimulationResultItem(agent, Parameters.RESOURCE_USAGE, step_number, args[0])
        self.register_result(result)

    def knowledge_snapshot_listener(self, agent, step_number, value):
        """
        :type agent: BaseAgent
        :type step_number: int
        :type value:
        """
        result = SimulationResultItem(agent, Parameters.KNOWLEDGE_SNAPSHOT, step_number, value)
        self.register_result(result)

    def knowledge_delta_listener(self, agent, step_number, delta):
        """
        :type agent: BaseAgent
        :type delta:
        :type step_number: int
        """
        result = SimulationResultItem(agent, Parameters.KNOWLEDGE_DELTA, step_number, delta)
        self.register_result(result)


class Parameters:
    RESOURCE_USAGE = 'Resource.Usage'
    KNOWLEDGE_SNAPSHOT = 'Knowledge.Snapshot'
    KNOWLEDGE_DELTA = 'Knowledge.Delta'