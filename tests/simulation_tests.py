import unittest

from unittest import mock
from unittest.mock import patch
from agents.competency import Competency
from agents.resource import Resource
from simulation_engine.simulation import Simulation


class SimulationTests(unittest.TestCase):
    def test_initialization(self):
        competencies = [Competency('A'), Competency('B')]
        resources = [
            Resource('A', {Competency('A'): 0, Competency('B'): 0.5}),
            Resource('B', {Competency('A'): 0.5, Competency('B'): 0}),
        ]

        sim_input = mock.Mock(spec=True)
        sim_input.competencies = mock.Mock(return_value=competencies)
        sim_input.resources = mock.Mock(return_value=resources)
        sim_input.students = mock.Mock(return_value=[])

        with patch("simulation.pub.subscribe") as subscribe_mock:
            simulation = Simulation(sim_input)

            subscribe_mock.assert_called_once_with()




