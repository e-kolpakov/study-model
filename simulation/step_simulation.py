import logging

__author__ = 'e.kolpakov'


class Simulation:
    def __init__(self):
        self._stop_condition = lambda x: False
        self._step = None

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
        pass

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


class SimulationState:
    def __init__(self):
        self._step = 0

    @property
    def step(self):
        """
        :rtype: int
        """
        return self._step
