import logging
import logging.config

from agents.student import Student
from study_model.competency import Competency
import log_config
from simulation_engine.simulation import Simulation
from simulation_input import get_simulation_input
from simulation_output import output_results


__author__ = 'john'


def perfect_knowledge_stop_condition(students, curriculum):
    """
    :type students: tuple[Student]
    :type curriculum: Curriculum
    """
    return all(
        competency.is_mastered(student.knowledge)
        for student in students
        for competency in curriculum.all_competencies())


def stop_condition(simulation_state):
    """
    :type simulation_state: SimulationState
    :rtype: bool
    """
    return perfect_knowledge_stop_condition(simulation_state.students, simulation_state.curriculum)


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


