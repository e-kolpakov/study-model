import logging
import logging.config

from log_config import log_config
from simulation_output import output_results
from simulation.simulation import stop_condition, Simulation, SimulationResult
from simulation.simulation_input import get_simulation_input


__author__ = 'e.kolpakov'


if __name__ == "__main__":
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    logger.debug("Starting...")

    simulation_input = get_simulation_input()

    logger.debug("Initializing simulation")
    simulation = Simulation(simulation_input)

    logger.debug("Initializing result collector")
    result = SimulationResult()

    logger.debug("Starting simulation")
    simulation.run()

    logger.debug("Simulation finished, displaying results")
    output_results(result)