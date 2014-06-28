import logging
import logging.config

import log_config
from simulation_output import output_results
from mooc_simulation.simulation import stop_condition, MoocSimulation, MoocSimulationResult
from mooc_simulation.simulation_input import get_simulation_input


__author__ = 'e.kolpakov'


if __name__ == "__main__":
    logging.config.dictConfig(log_config.config)
    logger = logging.getLogger(__name__)
    logger.debug("Starting...")

    simulation_input = get_simulation_input()

    logger.debug("Initializing simulation")
    simulation = MoocSimulation(simulation_input)
    simulation.stop_condition = stop_condition

    logger.debug("Initializing result collector")
    result = MoocSimulationResult()

    logger.debug("Starting simulation")
    simulation.run()

    logger.debug("Simulation finished, displaying results")
    output_results(result)