from collections import defaultdict
import logging

from pubsub import pub
from agents.resource_factory import ResourceFactory
from agents.student_factory import StudentFactory

from simulation_result import SimulationResult
from agents.resource import Resource
from resource_lookup_service import ResourceLookupService
from simulation_state import SimulationState
from topics import Topics


__author__ = 'john'


class Simulation(object):
    def __init__(self, sim_spec):
        """
        :type sim_spec: SimulationSpecification
        """
        self._step = 0
        """ :type: int """

        student_factory = StudentFactory(sim_spec.course_competencies)
        resource_factory = ResourceFactory(sim_spec.course_competencies)

        self._students = [student_factory.produce(spec) for spec in sim_spec.students]
        self._resources = [resource_factory.produce(spec) for spec in sim_spec.resources]
        self._competencies = sim_spec.course_competencies

        self._stop_condition = lambda x: False
        self._lookup_service = None
        """ :type: ResourceLookupService | None """

        self._results = defaultdict(lambda: SimulationResult(self.step))
        """ :type: dict[int, SimulationResult] """

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

    def resource_usage_listener(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        """
        self.current_step_result.add_resource_usage(resource)

    def knowledge_snapshot_listener(self, student, knowledge):
        """
        :type student: Student
        :type knowledge: dict[str, double]
        """
        self.current_step_result.register_knowledge_snapshot(student, knowledge)

    def knowledge_delta_listener(self, student, knowledge_delta):
        """
        :type student: Student
        :type knowledge_delta: dict[str, double]
        """
        self.current_step_result.register_knowledge_delta(student, knowledge_delta)

    def _initialize(self):
        self._lookup_service = ResourceLookupService(tuple(self._resources))
        for student in self._students:
            student.resource_lookup_service = self._lookup_service

        pub.subscribe(self.resource_usage_listener, Topics.RESOURCE_USAGE)
        pub.subscribe(self.knowledge_snapshot_listener, Topics.KNOWLEDGE_SNAPSHOT)
        pub.subscribe(self.knowledge_delta_listener, Topics.KNOWLEDGE_DELTA)

    def _grant_initial_access_rights(self):
        for student in self._students:
            for resource in self._resources:
                self._lookup_service.grant_access(student, resource)

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

    @property
    def results(self):
        """
        :rtype: dict[int, SimulationResult]
        """
        return self._results