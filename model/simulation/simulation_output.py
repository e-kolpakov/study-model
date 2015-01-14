from io import StringIO
from collections import OrderedDict, defaultdict
from itertools import groupby
import json

from model.simulation.result import ResultTopics


def _sort_and_group(sequence, key):
    return groupby(sorted(sequence, key=key), key=key)


class OutputRenderer:
    def __init__(self, output_stream, conf=None):
        self._output_stream = output_stream
        self.config = conf if conf else defaultdict(lambda: False)

    def _print(self, value, output_stream=None, newline=True):
        output_stream = output_stream if output_stream else self._output_stream
        output_stream.write(value)
        if newline:
            output_stream.write("\n")


class HumanReadableOutputRenderer(OutputRenderer):
    def _handler_map(self):
        return OrderedDict([
            ('resource_usage', self.print_resource_usages),
            ('snapshots', self.print_snapshots),
            ('deltas', self.print_deltas),
            ('counts', self.print_counts),
            ('exam_feedbacks', self.print_exams),
        ])

    def render(self, results):
        for key, handler in self._handler_map().items():
            if self.config.get(key, False):
                self._print(handler(results))

    def print_resource_usages(self, results):
        with StringIO() as result_stream:
            self._print("=== Resources START ===", result_stream)
            resource_usages = results.get_parameter(ResultTopics.RESOURCE_USAGE)
            for agent_name, group in _sort_and_group(resource_usages, key=lambda record: record.agent.name):
                for item in sorted(group, key=lambda record: record.time):
                    self._print(
                        "Student {student} used {resource} at {time}".format(
                            resource=item.value.name, student=agent_name, time=item.time
                        ),
                        result_stream
                    )
            self._print("==== Resources END ====", result_stream)
            return result_stream.getvalue()

    def print_snapshots(self, results):
        with StringIO() as result_stream:
            self._print("=== Snapshots START ===", result_stream)
            snaps = results.get_parameter(ResultTopics.KNOWLEDGE_SNAPSHOT)
            for item in snaps:
                snapshot_str = ", ".join(list(map(str, sorted(item.value, key=lambda fact: fact.code))))
                self._print(
                    "Student {name} at {time}: {snapshot}".format(
                        name=item.agent.name, snapshot=snapshot_str, time=item.time
                    ),
                    result_stream
                )
            self._print("==== Snapshots END ====", result_stream)
            return result_stream.getvalue()

    def print_deltas(self, results):
        with StringIO() as result_stream:
            self._print("===== Delta START =====", result_stream)
            delta = results.get_parameter(ResultTopics.KNOWLEDGE_DELTA)
            for item in delta:
                delta_str = ", ".join(list(map(str, item.value)))
                self._print(
                    "Student {name} at {time}: {delta}".format(name=item.agent.name, delta=delta_str, time=item.time),
                    result_stream
                )
            self._print("====== Delta END ======", result_stream)
            return result_stream.getvalue()

    def print_counts(self, results):
        with StringIO() as result_stream:
            self._print("===== Count START =====", result_stream)
            counts = results.get_parameter(ResultTopics.KNOWLEDGE_COUNT)
            for item in counts:
                self._print(
                    "Student {name} at {time}: {count}".format(name=item.agent.name, count=item.value, time=item.time),
                    result_stream
                )
            self._print("====== Count END ======", result_stream)
            return result_stream.getvalue()

    def print_exams(self, results):
        with StringIO() as result_stream:
            self._print("== Exam Results START ==", result_stream)
            exam_results = results.get_parameter(ResultTopics.EXAM_RESULTS)
            for item in exam_results:
                feedback = item.value
                self._print(
                    "Student {name} taken {exam} at {time} and got {grade} ({passed})"
                    .format(
                        name=item.agent.name, exam=feedback.exam.code, time=item.time,
                        grade=feedback.grade, passed="passed" if feedback.passed else "not passed"
                    ),
                    result_stream
                )
            self._print("=== Exam Results End ===", result_stream)
            return result_stream.getvalue()


class JsonOutputRenderer(OutputRenderer):
    def __init__(self, output_stream, config=None, pretty_print=True):
        super().__init__(output_stream, config)
        self._pretty_print = pretty_print

    def render(self, results):
        result = OrderedDict()
        handler_map = OrderedDict([
            ('resource_usage', self.get_resource_access),
            ('snapshots', self.get_snapshots),
            ('deltas', self.get_deltas),
            ('counts', self.get_counts),
            ('exam_feedbacks', self.get_exam_feedbacks),
        ])

        for key, handler in handler_map.items():
            if self.config.get(key, False):
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

    def get_resource_access(self, results):
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
        return self.time_series(results, ResultTopics.KNOWLEDGE_COUNT, value_transform=int)

    def get_exam_feedbacks(self, results):
        result = OrderedDict()
        exam_feedbacks = results.get_parameter(ResultTopics.EXAM_RESULTS)
        for exam, group in _sort_and_group(exam_feedbacks, key=lambda item: item.value.exam):
            result[exam.code] = {}
            for agent, items in _sort_and_group(group, key=lambda item: item.agent):
                result[exam.code][agent.name] = {item.time: (item.value.grade, item.value.passed) for item in items}
        return result