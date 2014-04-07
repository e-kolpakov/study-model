from collections import defaultdict
import logging

from pubsub import pub

from simulation_engine.competency_lookup_service import CompetencyLookupService
from simulation_engine.simulation_result import SimulationResult
from agents.resource import Resource
from simulation_engine.resource_lookup_service import ResourceLookupService
from simulation_engine.simulation_state import SimulationState
from simulation_engine.topics import Topics


__author__ = 'john'


class Simulation(ResourceLookupService, CompetencyLookupService):
    def __init__(self, simulation_input, *args, **kwargs):
        """
        :type simulation_input: SimulationInput
        """
        super(Simulation, self).__init__(*args, **kwargs)

        self._step = 0
        """ :type: int """

        self._students = simulation_input.students
        """ :type: list[Student] """
        self._resources = simulation_input.resources
        """ :type: list[Resource] """
        self._competencies = simulation_input.competencies
        """ :type: list[Competency] """

        self._stop_condition = lambda x: False
        self._lookup_service = None
        """ :type: ResourceLookupService | None """

        self._results = defaultdict(lambda: SimulationResult(self.step))
        """ :type: dict[int, SimulationResult] """

        self._build_competency_lookup(self._competencies)
        self._register_resources(self._resources)

    @property
    def step(self):
        """
        :rtype: int
        """
        return self._step

    @property
    def students(self):
        """
        :rtype: tuple[Student]
        """
        return tuple(self._students)

    @property
    def resources(self):
        """
        :rtype: tuple[Resource]
        """
        return tuple(self._resources)

    @property
    def competencies(self):
        """
        :rtype: tuple[str]
        """
        return tuple(self._competencies)

    @property
    def state(self):
        return SimulationState(self.students, self.resources, self.competencies)

    @property
    def stop_condition(self):
        """
        :rtype: callable(SimulationState)
        """
        return self._stop_condition

    @stop_condition.setter
    def stop_condition(self, value):
        """
        :type value: callable(SimulationState)
        """
        self._stop_condition = value

    @property
    def current_step_result(self):
        """
        :rtype: SimulationResult
        """
        return self._results[self.step]

    @property
    def results(self):
        """
        :rtype: dict[int, SimulationResult]
        """
        return self._results

    def resource_usage_listener(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        """
        self.current_step_result.add_resource_usage(resource)

    def knowledge_snapshot_listener(self, student, competencies):
        """
        :type student: Student
        :type competencies: dict[Competency, double]
        """
        self.current_step_result.register_knowledge_snapshot(student, competencies)

    def knowledge_delta_listener(self, student, competency_delta):
        """
        :type student: Student
        :type competency_delta: dict[Competency, double]
        """
        self.current_step_result.register_knowledge_delta(student, competency_delta)

    def _initialize(self):
        for student in self._students:
            student.resource_lookup_service = self
            student.competency_lookup_service = self

        pub.subscribe(self.resource_usage_listener, Topics.RESOURCE_USAGE)
        pub.subscribe(self.knowledge_snapshot_listener, Topics.KNOWLEDGE_SNAPSHOT)
        pub.subscribe(self.knowledge_delta_listener, Topics.KNOWLEDGE_DELTA)

    def _grant_initial_access_rights(self):
        for student in self._students:
            for resource in self._resources:
                self.grant_access(student, resource)

    def run(self):
        self._initialize()
        self._grant_initial_access_rights()
        logger = logging.getLogger(__name__)
        while not self.stop_condition(self.state):
            logger.info("Starting step {step_no}".format(step_no=self._step))
            self._step += 1
            for student in self._students:
                student.study()
            logger.info("Finalizing step {step_no}".format(step_no=self._step))