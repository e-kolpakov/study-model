from collections import OrderedDict, defaultdict
from itertools import groupby
import json

from simulation.result import ResultTopics


def _sort_and_group(sequence, key):
    return groupby(sorted(sequence, key=key), key=key)


class OutputRenderer:
    def __init__(self, output_stream, resourse_access=True, snapshots=True, deltas=True, counts=True):
        self._output_stream = output_stream
        self.resourse_access = resourse_access
        self.snapshots = snapshots
        self.deltas = deltas
        self.counts = counts

    def _print(self, value, newline=True):
        self._output_stream.write(value)
        if newline:
            self._output_stream.write("\n")


class HumanReadableOutputRenderer(OutputRenderer):
    def render(self, results):
        if self.resourse_access:
            self.print_resource_usages(results)
        if self.snapshots:
            self.print_snapshots(results)
        if self.deltas:
            self.print_deltas(results)
        if self.counts:
            self.print_counts(results)

    def print_resource_usages(self, results):
        self._print("=== Resources START ===")
        resource_usages = results.get_parameter(ResultTopics.RESOURCE_USAGE)
        for agent_name, group in _sort_and_group(resource_usages, key=lambda record: record.agent.name):
            for item in sorted(group, key=lambda record: record.time):
                self._print("Student {student} used {resource} at {time}".format(
                    resource=item.value.name, student=agent_name, time=item.time))
        self._print("==== Resources END ====")

    def print_snapshots(self, results):
        self._print("=== Snapshots START ===")
        snaps = results.get_parameter(ResultTopics.KNOWLEDGE_SNAPSHOT)
        for item in snaps:
            snapshot_str = ", ".join(list(map(str, sorted(item.value, key=lambda fact: fact.code))))
            self._print(
                "Student {name} at {time}: {snapshot}".format(name=item.agent.name, snapshot=snapshot_str, time=item.time))
        self._print("==== Snapshots END ====")

    def print_deltas(self, results):
        self._print("===== Delta START =====")
        delta = results.get_parameter(ResultTopics.KNOWLEDGE_DELTA)
        for item in delta:
            delta_str = ", ".join(list(map(str, item.value)))
            self._print("Student {name} at {time}: {delta}".format(name=item.agent.name, delta=delta_str, time=item.time))
        self._print("====== Delta END ======")

    def print_counts(self, results):
        self._print("===== Count START =====")
        counts = results.get_parameter(ResultTopics.KNOWLEDGE_COUNT)
        for item in counts:
            self._print("Student {name} at {time}: {count}".format(name=item.agent.name, count=item.value, time=item.time))
        self._print("====== Count END ======")


class JsonOutputRenderer(OutputRenderer):
    def __init__(self, output_stream, resourse_access=True, snapshots=True, deltas=True, counts=True, pretty_print=True):
        super().__init__(output_stream, resourse_access, snapshots, deltas, counts)
        self._pretty_print = pretty_print

    def render(self, results):
        result = OrderedDict()
        handler_map = OrderedDict([
            ('resourse_usage', (lambda: self.resourse_access, self.get_resourse_access)),
            ('snapshots', (lambda: self.snapshots, self.get_snapshots)),
            ('deltas', (lambda: self.deltas, self.get_deltas)),
            ('counts', (lambda: self.counts, self.get_counts)),
        ])

        for key, (predicate, handler) in handler_map.items():
            if predicate():
                result[key] = handler(results)
        result = json.dumps(result, indent=2) if self._pretty_print else json.dumps(result)
        self._print(result)

    def time_series(self, results, parameter, value_transform=None):
        result = defaultdict(OrderedDict)
        agents = results.agents
        for agent in agents:
            time_series = results.get_time_series(parameter, agent)
            for item in time_series:
                result[agent.name][item.time] = value_transform(item.value)
        return result

    def get_resourse_access(self, results):
        result = OrderedDict()
        resource_usages = results.get_parameter(ResultTopics.RESOURCE_USAGE)
        for time, group in _sort_and_group(resource_usages, key=lambda item: item.time):
            result[time] = {}
            for resource, items in _sort_and_group(group, key=lambda item: item.value):
                result[time][resource.name] = list(map(lambda item: item.agent.name, items))
        return result

    def get_snapshots(self, results):
        value = lambda facts: [fact.code for fact in facts]
        return self.time_series(results, ResultTopics.KNOWLEDGE_SNAPSHOT, value_transform=value)

    def get_deltas(self, results):
        value = lambda facts: [fact.code for fact in facts]
        return self.time_series(results, ResultTopics.KNOWLEDGE_DELTA, value_transform=value)

    def get_counts(self, results):
        value = lambda facts: [fact.code for fact in facts]
        return self.time_series(results, ResultTopics.KNOWLEDGE_COUNT, value_transform=int)