__author__ = 'john'


class SimulationResult(object):
    def __init__(self):
        self._results = list()
        """:type: list[ResultRecord]"""

    def register_result(self, result_record):
        """
        :type result_record: ResultRecord
        :rtype: None
        """
        self._results.append(result_record)

    @property
    def results(self):
        """
        :rtype: tuple[ResultRecord]
        """
        return self._results

    def time_slice(self, timestamp):
        return (result for result in self.results if result.timestamp == timestamp)

    def key_slice(self, key):
        return (result for result in self.results if result.key == key)


