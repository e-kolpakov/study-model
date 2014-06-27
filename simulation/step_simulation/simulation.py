import logging
from simulation.agents.base_agent import BaseAgent

__author__ = 'e.kolpakov'


class Simulation:
    def __init__(self):
        self._stop_condition = lambda x: False
        self._step = None
        self._agents = {}
        """ :type: dict[str, BaseAgent] """

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
        for agent_id, agent in self._agents.items():
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
            self._step += 1
            logger.info("Starting step {step_no}".format(step_no=self._step))
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
            if agent.agent_id in self._agents:
                msg = "Agent with the id {0} already registered".format(agent.agent_id)
                logger.error(msg)
                raise ValueError(msg)
            self._agents[agent.agent_id] = agent


class SimulationState:
    def __init__(self):
        self._step = 0

    @property
    def step(self):
        """
        :rtype: int
        """
        return self._step

