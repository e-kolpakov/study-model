from pubsub import pub
from output.output_specification.result_record import ResultRecord
from output.output_specification.simulation_result import SimulationResult

__author__ = 'john'


class OutputCollector(object):
    def __init__(self, output_spec):
        """
        :type output_spec: OutputSpecification
        """
        self._output_spec = output_spec
        self._simulation_result = SimulationResult()
        self.register_consumers()

    def register_consumers(self):
        for observable in self._output_spec.observables:
            pub.subscribe(self._result_listener, observable.key)

    def _result_listener(self, key, timestamp, value):
        self._simulation_result.register_result(ResultRecord(key, timestamp, value))

    def get_results(self):
        return self._simulation_result