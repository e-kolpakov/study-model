import logging
import logging.config

import log_config
from study_model.simulation_engine import Simulation
from study_model.simulation_input import get_simulation_input
from simulation_output import output_results


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


