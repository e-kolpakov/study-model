import logging
import logging.config
from agents.behaviors.factory import BehaviorFactory

import log_config
from simulation import Simulation
from simulation_specification.resource_specification import ResourceSpecification
from simulation_specification.simulation_specification import SimulationSpecification
from simulation_specification.student_specification import StudentSpecification
from simulation_state import SimulationState
from simulation_result import SimulationResult

__author__ = 'john'


def read_simulation_spec():
    """
    :rtype: SimulationSpecification
    """
    sim_spec = SimulationSpecification()
    sim_spec.course_competencies.extend(['algebra', 'calculus', 'diff_eq'])

    zero_knowledge = {competency: 0 for competency in sim_spec.course_competencies}

    sim_spec.students.append(
        StudentSpecification("John", zero_knowledge, {'resource_choice': 'rational'}, agent_id='s1'))
    sim_spec.students.append(
        StudentSpecification("Jim", zero_knowledge, {'resource_choice': 'rational'}, agent_id='s2'))
    sim_spec.resources.append(
        ResourceSpecification("Resource1", {'algebra': 1.0, 'calculus': 0.2, 'diff_eq': 0}, 'basic', agent_id='r1')
    )
    sim_spec.resources.append(
        ResourceSpecification("Resource1", {'algebra': 0.0, 'calculus': 0.8, 'diff_eq': 1.0}, 'basic', agent_id='r2')
    )
    return sim_spec


def perfect_knowledge_stop_condition(students, competencies):
    """
    :type students: tuple[Student]
    :type competencies: tuple[str]
    """
    perfect_knowledge = lambda student: all(
        knowledge >= 1.0 for competency, knowledge in student.get_knowledge(competencies).items()
    )
    return all(perfect_knowledge(student) for student in students)


def stop_condition(simulation_state):
    """
    :type simulation_state: SimulationState
    :rtype: bool
    """
    return perfect_knowledge_stop_condition(simulation_state.students, simulation_state.competencies)


def output_results(results):
    """
    :type results: dict[int, SimulationResult]
    """
    for step, result in results.items():
        print("======= Step {step} =======".format(step=step))
        for resource, usage in result.resource_usage.items():
            print("Resource {name} used {times}".format(name=resource, times=usage))
        print("=== Snapshots ===")
        for student, snapshot in result.knowledge_snapshot.items():
            print("Student {name}: {snapshot}".format(name=student, snapshot=snapshot))
        print("===== Delta =====")
        for student, delta in result.knowledge_delta.items():
            print("Student {name}: {delta}".format(name=student, delta=delta))
        print("===== Step {step} End =====".format(step=step))


if __name__ == "__main__":
    logging.config.dictConfig(log_config.config)
    logger = logging.getLogger(__name__)
    logger.debug("Starting...")

    logger.debug("Initializing behavior factory...")
    behavior_factory = BehaviorFactory()

    sim_spec = read_simulation_spec()

    logger.debug("Initializing simulation")
    simulation = Simulation(sim_spec)
    simulation.stop_condition = stop_condition

    logger.debug("Starting simulation")
    simulation.run()
    output_results(simulation.results)


