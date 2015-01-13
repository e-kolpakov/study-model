import logging
import logging.config
import sys
import os

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
    output_config = {
        'resourse_usage': True,
        'snapshots': True,
        'deltas': True,
        'counts': True,
        'exam_feedbacks': True
    }

    os.makedirs("results", exist_ok=True)
    with open("results/result.json", 'w+') as json_result:
        json_renderer = JsonOutputRenderer(json_result, output_config)
        json_renderer.render(result)

    with open("results/result.txt", 'w+') as txt_result:
        human_renderer = HumanReadableOutputRenderer(txt_result, output_config)
        human_renderer.render(result)
