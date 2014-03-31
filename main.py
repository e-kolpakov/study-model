import logging
import logging.config
from agents.behaviors import RationalResourceChoiceBehavior

from agents.behaviors.student.behavior_group import BehaviorGroup
from agents.resource import Resource
from agents.student import Student

import log_config
from simulation import Simulation
from simulation_input import SimulationInput
from simulation_state import SimulationState
from simulation_result import SimulationResult

__author__ = 'john'


def get_simulation_input():
    """
    :rtype: SimulationInput
    """
    sim_input = SimulationInput()
    sim_input.competencies.extend(['algebra', 'calculus', 'diff_eq'])

    zero_knowledge = {competency: 0 for competency in sim_input.competencies}

    rational_behavior = BehaviorGroup()
    rational_behavior.resource_choice = RationalResourceChoiceBehavior()

    sim_input.students.append(
        Student("John", zero_knowledge, rational_behavior, agent_id='s1'))
    sim_input.students.append(
        Student("Jim", {}, rational_behavior, agent_id='s2'))
    sim_input.resources.append(
        Resource("Resource1", {'algebra': 1.0, 'calculus': 0.2, 'diff_eq': 0}, 'basic', agent_id='r1')
    )
    sim_input.resources.append(
        Resource("Resource1", {'algebra': 0.0, 'calculus': 0.8, 'diff_eq': 1.0}, 'basic', agent_id='r2')
    )
    return sim_input


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

    simulation_input = get_simulation_input()

    logger.debug("Initializing simulation")
    simulation = Simulation(simulation_input)
    simulation.stop_condition = stop_condition

    logger.debug("Starting simulation")
    simulation.run()
    output_results(simulation.results)


