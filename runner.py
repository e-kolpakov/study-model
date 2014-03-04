from agents.resource import Resource
from services.student_factory import StudentFactory

__author__ = 'john'


class Runner(object):
    def __init__(self, simulation_spec):
        """
        :param SimulationSpecification simulation_spec: Simulation specification
        """
        self.__spec = simulation_spec

        self._students_lookup = None
        """ :type: dict[str, Student] """
        self._resources_lookup = None
        """ :type: dict[str, Resource] """
        self._course_competencies = None
        """ :type: list[str] """

        self._student_factory = StudentFactory()
        """ :type: StudentFactory """

    def run(self):
        pass

    def initialize(self):
        self._course_competencies = self.__spec.course_competencies
        self._create_students(self.__spec.students)
        self._create_resources(self.__spec.resources)

    def _create_students(self, students_spec):
        """
        Parses resource specification and creates student agents
        :param list[StudentSpecification] students_spec: Student specifications
        :rtype: None
        """
        students = (self._student_factory.create_student(spec, self._course_competencies) for spec in students_spec)
        self._students_lookup = {student.agent_id: student for student in students}

    def _create_resources(self, resources_spec):
        """
        Parses resource specification and creates resource agents
        :param list[ResourceSpecification resources_spec: Resources Specification
        :rtype: None
        """
        resources = (Resource(spec) for spec in resources_spec)
        self._resources_lookup = {resource.agent_id: resource for resource in resources}

