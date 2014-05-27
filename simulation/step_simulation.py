import logging
from simulation.agents.base_agent import BaseAgent

__author__ = 'e.kolpakov'


class Simulation:
    def __init__(self):
        self._stop_condition = lambda x: False
        self._step = None
        self._agents = []
        """ :type: list[BaseAgent] """

    @property
    def step(self):
        """
        :rtype: int
        """
        return self._step

    @property
    def stop_condition(self):
        """
        :rtype: callable(SimulationState)
        """
        return self._stop_condition

    @stop_condition.setter
    def stop_condition(self, value):
        """
        :type value: callable(SimulationState)
        """
        self._stop_condition = value

    def initialize(self):
        self._step = 0

    def _execute_step(self):
        for agent in self._agents:
            agent.execute_step(self.step)

    @property
    def state(self):
        """
        :rtype: SimulationState
        """
        raise NotImplemented

    def run(self):
        self.initialize()
        logger = logging.getLogger(__name__)
        while not self.stop_condition(self.state):
            logger.info("Starting step {step_no}".format(step_no=self._step))
            self._step += 1
            self._execute_step()
            logger.info("Finalizing step {step_no}".format(step_no=self._step))

    def _register_agents(self, agents):
        """
        Registers agents in simulation
        :param agents: list[BaseAgent] | tuple[BaseAgent]
        """
        logger = logging.getLogger(__name__)
        for agent in agents:
            if not isinstance(agent, BaseAgent):
                msg = "Instance of BaseAgent subclass expected, got {0}".format(agent)
                logger.error(msg)
                raise ValueError(msg)
            self._agents.append(agent)


class SimulationState:
    def __init__(self):
        self._step = 0

    @property
    def step(self):
        """
        :rtype: int
        """
        return self._step