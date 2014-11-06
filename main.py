import logging
import logging.config
import sys

from log_config import log_config
from simulation.simulation_output import HumanReadableOutputRenderer, JsonOutputRenderer
from simulation.simulation import Simulation
from simulation.result import SimulationResult
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
    output_renderer = HumanReadableOutputRenderer(sys.stdout)
    output_renderer.render(result)