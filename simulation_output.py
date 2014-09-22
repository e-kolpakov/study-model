from itertools import groupby

from simulation.result import ResultTopics


__author__ = 'e.kolpakov'

snapshots = True
deltas = True
counts = True


def output_results(results):
    """
    :type results: SimulationResult
    """
    # pass
    print_resource_usages(results)
    if snapshots:
        print_snapshots(results)
    if deltas:
        print_deltas(results)
    if counts:
        print_counts(results)

def print_resource_usages(results):
    print("=== Resources START ===")
    resource_usages = results.get_parameter(ResultTopics.RESOURCE_USAGE)
    for (resource, time), group in groupby(resource_usages, key=lambda item: (item.value, item.time)):
        used_by = ", ".join(map(lambda item: item.agent.name, group))
        print("Resource {name} used by {used_by} at {time}".format(name=resource.name, used_by=used_by, time=time))
    print("==== Resources END ====")


def print_snapshots(results):
    print("=== Snapshots START ===")
    snaps = results.get_parameter(ResultTopics.KNOWLEDGE_SNAPSHOT)
    for item in snaps:
        snapshot_str = ", ".join(list(map(str, item.value)))
        print(
            "Student {name} at {time}: {snapshot}".format(name=item.agent.name, snapshot=snapshot_str, time=item.time))
    print("==== Snapshots END ====")


def print_deltas(results):
    print("===== Delta START =====")
    delta = results.get_parameter(ResultTopics.KNOWLEDGE_DELTA)
    for item in delta:
        delta_str = ", ".join(list(map(str, item.value)))
        print("Student {name} at {time}: {delta}".format(name=item.agent.name, delta=delta_str, time=item.time))
    print("====== Delta END ======")


def print_counts(results):
    print("===== Count START =====")
    counts = results.get_parameter(ResultTopics.KNOWLEDGE_COUNT)
    for item in counts:
        print("Student {name} at {time}: {count}".format(name=item.agent.name, count=item.value, time=item.time))
    print("====== Count END ======")