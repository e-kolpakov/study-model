from collections import defaultdict

from pubsub import pub

from simulation.step_simulation import Simulation, SimulationState
from study_model.mooc_simulation.resource_lookup_service import ResourceLookupService


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

        self._lookup_service = None
        """ :type: ResourceLookupService | None """

        self._results = defaultdict(lambda: MoocSimulationResult(self.step))
        """ :type: dict[int, SimulationResult] """

        self._register_resources(self._resources)

        self._register_agents(self._students)
        self._register_agents(self._resources)

    @property
    def state(self):
        """
        :rtype: MoocSimulationState
        """
        return MoocSimulationState(self._students, self._resources, self._curriculum)

    @property
    def current_step_result(self):
        """
        :rtype: MoocSimulationResult
        """
        return self._results[self.step]

    @property
    def results(self):
        """
        :rtype: dict[int, MoocSimulationResult]
        """
        return self._results

    def resource_usage_listener(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        """
        self.current_step_result.add_resource_usage(resource)

    def knowledge_snapshot_listener(self, agent, value, step_number):
        """
        :type agent: BaseAgent
        :type value:
        :type step_number: int
        """
        self.current_step_result.register_knowledge_snapshot(agent, value)

    def knowledge_delta_listener(self, agent, delta, step_number):
        """
        :type agent: BaseAgent
        :type delta:
        :type step_number: int
        """
        self.current_step_result.register_knowledge_delta(agent, delta)

    def initialize(self):
        for student in self._students:
            student.resource_lookup_service = self
            student.curriculum = self._curriculum

        pub.subscribe(self.resource_usage_listener, Topics.RESOURCE_USAGE)
        pub.subscribe(self.knowledge_snapshot_listener, Topics.KNOWLEDGE_SNAPSHOT)
        pub.subscribe(self.knowledge_delta_listener, Topics.KNOWLEDGE_DELTA)

        for student in self._students:
            for resource in self._resources:
                self.grant_access(student, resource)


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
        """
        :rtype: tuple(Student)
        """
        return tuple(self._students)

    @property
    def resources(self):
        """
        :rtype: tuple[Resource]
        """
        return tuple(self._resources)

    @property
    def curriculum(self):
        """
        :rtype: Curriculum
        """
        return self._curriculum


class MoocSimulationResult:
    def __init__(self, simulation_step):
        self._simulation_step = simulation_step
        self._resource_usage = defaultdict(int)
        self._knowledge = dict()
        self._new_knowledge = dict()

    def add_resource_usage(self, resource):
        """
        :type resource: Resource
        """
        self._resource_usage[resource.name] += 1

    def register_knowledge_snapshot(self, student, knowledge):
        """
        :type student: BaseAgent
        :type knowledge: set[Fact]
        """
        self._knowledge[student.agent_id] = knowledge

    def register_knowledge_delta(self, student, new_knowledge):
        """
        :type student: BaseAgent
        :type new_knowledge: set[Fact]
        """
        self._new_knowledge[student.agent_id] = new_knowledge

    @property
    def resource_usage(self):
        return self._resource_usage

    @property
    def knowledge(self):
        return self._knowledge

    @property
    def new_knowledge(self):
        return self._new_knowledge


class Topics:
    RESOURCE_USAGE = 'Resource.Usage'
    KNOWLEDGE_SNAPSHOT = 'Knowledge.Snapshot'
    KNOWLEDGE_DELTA = 'Knowledge.Delta'