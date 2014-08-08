from pubsub import pub

__author__ = 'e.kolpakov'


class SimulationResultItem:
    def __init__(self, agent, parameter, time, value):
        self._agent = agent
        self._parameter = parameter
        self._time = time
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
    def time(self):
        return self._time

    @property
    def value(self):
        return self._value

    def __unicode__(self):
        return u"{agent}.{parameter}[{step}] = {value}".format(
            agent=str(self.agent), parameter=self.parameter, step=self.time, value=self.value)

    def __str__(self):
        return self.__unicode__()


class SimulationResultBase:
    def __init__(self):
        self._results = []
        """ :type: list[SimulationResultItem] """

    @staticmethod
    def _register_result_handler(callback, parameter):
        pub.subscribe(callback, parameter)

    def register_result(self, result_item):
        """
        :param result_item: SimulationResultItem
        :return: None
        """
        self._results.append(result_item)

    def _get_data(self, filter_callback):
        """
        :param filter_callback: (SimulationResultItem) -> bool
        :return: list[SimulationResultItem]
        """
        return (item for item in self._results if filter_callback(item))

    def get_parameter(self, parameter):
        items = self._get_data(lambda item: item.parameter == parameter)
        return sorted(items, key=lambda item: (item.time, item.agent.agent_id))

    def get_time_series(self, parameter, agent):
        items = self._get_data(lambda item: item.agent == agent and item.parameter == parameter)
        return sorted(items, key=lambda item: item.time)

    def get_time_slice(self, parameter, step):
        items = self._get_data(lambda item: item.step == step and item.parameter == parameter)
        return sorted(items, key=lambda item: item.agent.agent_id)


class SimulationResult(SimulationResultBase):
    def __init__(self):
        super(SimulationResult, self).__init__()

    def __init__(self):
        super(SimulationResult, self).__init__()
        pub.subscribe(self.resource_usage_listener, ResultTopics.RESOURCE_USAGE)
        pub.subscribe(self.knowledge_snapshot_listener, ResultTopics.KNOWLEDGE_SNAPSHOT)
        pub.subscribe(self.knowledge_delta_listener, ResultTopics.KNOWLEDGE_DELTA)

    def resource_usage_listener(self, agent, time, args, kwargs):
        """
        :param agent: BaseAgent
        :param step_number: int
        :param args: list[Any]
        :param kwargs: dict[str, Any]
        :return:
        """
        self.register_result(SimulationResultItem(agent, ResultTopics.RESOURCE_USAGE, time, args[0]))


    def knowledge_snapshot_listener(self, agent, time, value):
        """
        :type agent: BaseAgent
        :type step_number: int
        :type value:
        """
        self.register_result(SimulationResultItem(agent, ResultTopics.KNOWLEDGE_SNAPSHOT, time, value))

    def knowledge_delta_listener(self, agent, time, delta):
        """
        :type agent: BaseAgent
        :type delta:
        :type step_number: int
        """
        self.register_result(SimulationResultItem(agent, ResultTopics.KNOWLEDGE_DELTA, time, delta))


class ResultTopics:
    RESOURCE_USAGE = 'Resource.Usage'
    KNOWLEDGE_SNAPSHOT = 'Knowledge.Snapshot'
    KNOWLEDGE_DELTA = 'Knowledge.Delta'
