from pubsub import pub

__author__ = 'e.kolpakov'


class SimulationResultItem:
    def __init__(self, agent, parameter, step, value):
        self._agent = agent
        self._parameter = parameter
        self._step = step
        self._value = value

    @property
    def agent(self):
        """
        :return: BaseAgent
        """
        return self._agent

    @property
    def parameter(self):
        return self._parameter

    @property
    def step(self):
        return self._step

    @property
    def value(self):
        return self._value

    def __unicode__(self):
        return u"{agent}.{parameter}[{step}] = {value}".format(
            agent=str(self.agent), parameter=self.parameter, step=self.step, value=self.value)

    def __str__(self):
        return self.__unicode__()


# TODO: use indices or some kind of OLAP approach to speed up queries
class SimulationResult:
    def __init__(self):
        self._results = []
        """ :type: list[SimulationResultItem] """

        self._max_step = 0

    @staticmethod
    def _register_result_handler(callback, parameter):
        pub.subscribe(callback, parameter)

    @property
    def max_step(self):
        return self._max_step

    def register_result(self, result_item):
        """
        :param result_item: SimulationResultItem
        :return: None
        """
        self._results.append(result_item)
        self._max_step = max(self._max_step, result_item.step)

    def _get_data(self, filter_callback):
        """
        :param filter_callback: (SimulationResultItem) -> bool
        :return: list[SimulationResultItem]
        """
        return (item for item in self._results if filter_callback(item))

    def get_time_series(self, parameter, agent):
        items = self._get_data(lambda item: item.agent == agent and item.parameter == parameter)
        return sorted(items, key=lambda item: item.step)

    def get_time_slice(self, parameter, step):
        items = self._get_data(lambda item: item.step == step and item.parameter == parameter)
        return sorted(items, key=lambda item: item.agent.agent_id)