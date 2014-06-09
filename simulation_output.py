from itertools import groupby
from study_model.mooc_simulation.simulation import Parameters

__author__ = 'e.kolpakov'

snapshots = True
deltas = True


def output_results(results):
    """
    :type results: MoocSimulationResult
    """
    for step in range(1, results.max_step):
        print("======= Step {step} =======".format(step=step))
        print_resource_usages(results, step)
        if snapshots:
            print_snapshots(results, step)
        if deltas:
            print_deltas(results, step)
        print("===== Step {step} End =====".format(step=step))


def print_resource_usages(results, step):
    print("=== Resources ===")
    resource_usages = results.get_time_slice(Parameters.RESOURCE_USAGE, step)
    for resource, group in groupby(resource_usages, key=lambda item: item.value):
        used_by = ", ".join(map(lambda item: item.agent.name, group))
        print("Resource {name} used by {used_by}".format(name=resource.name, used_by=used_by))


def print_snapshots(results, step):
    print("=== Snapshots ===")
    snaps = results.get_time_slice(Parameters.KNOWLEDGE_SNAPSHOT, step)
    for item in snaps:
        snapshot_str = ", ".join(list(map(str, item.value)))
        print("Student {name}: {snapshot}".format(name=item.agent.name, snapshot=snapshot_str))


def print_deltas(results, step):
    print("===== Delta =====")
    delta = results.get_time_slice(Parameters.KNOWLEDGE_DELTA, step)
    for item in delta:
        delta_str = ", ".join(list(map(str, item.value)))
        print("Student {name}: {delta}".format(name=item.agent.name, delta=delta_str))
