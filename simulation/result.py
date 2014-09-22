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
        self._register_result_handler(self.resource_usage_listener, ResultTopics.RESOURCE_USAGE)
        self._register_result_handler(self.knowledge_snapshot_listener, ResultTopics.KNOWLEDGE_SNAPSHOT)
        self._register_result_handler(self.knowledge_delta_listener, ResultTopics.KNOWLEDGE_DELTA)
        self._register_result_handler(self.knowledge_count_listener, ResultTopics.KNOWLEDGE_COUNT)

    def resource_usage_listener(self, agent, args, kwargs):
        """
        :param agent: BaseAgent
        :param args: list[Any]
        :param kwargs: dict[str, Any]
        :return:
        """
        self.register_result(SimulationResultItem(agent, ResultTopics.RESOURCE_USAGE, agent.time, args[0]))

    def knowledge_snapshot_listener(self, agent, value):
        """
        :type agent: BaseAgent
        :type value:
        """
        self.register_result(SimulationResultItem(agent, ResultTopics.KNOWLEDGE_SNAPSHOT, agent.time, value))

    def knowledge_delta_listener(self, agent, delta):
        """
        :type agent: BaseAgent
        :type delta:
        """
        self.register_result(SimulationResultItem(agent, ResultTopics.KNOWLEDGE_DELTA, agent.time, delta))

    def knowledge_count_listener(self, agent, value):
        """
        :type agent: BaseAgent
        :type count:
        """
        self.register_result(SimulationResultItem(agent, ResultTopics.KNOWLEDGE_COUNT, agent.time, value))


class ResultTopics:
    RESOURCE_USAGE = 'Resource.Usage'
    KNOWLEDGE_SNAPSHOT = 'Knowledge.Snapshot'
    KNOWLEDGE_COUNT = 'Knowledge.Count'
    KNOWLEDGE_DELTA = 'Knowledge.Delta'
