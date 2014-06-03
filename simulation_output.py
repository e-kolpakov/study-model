__author__ = 'e.kolpakov'

snapshots = True
deltas = True


def output_results(results):
    """
    :type results: dict[int, MoocSimulationResult]
    """
    for step, result in results.items():
        print("======= Step {step} =======".format(step=step))
        for resource, usage in result.resource_usage.items():
            print("Resource {name} used {times} times".format(name=resource, times=usage))
        if snapshots:
            print("=== Snapshots ===")
            for student, snapshot in result.knowledge.items():
                # snapshot_str = ", ".join(list(map(str, snapshot)))
                print("Student {name}: {snapshot}".format(name=student, snapshot=snapshot))
        if deltas:
            print("===== Delta =====")
            for student, new_knowledge in result.new_knowledge.items():
                delta_str = ", ".join(list(map(str, new_knowledge)))
                print("Student {name}: {delta}".format(name=student, delta=delta_str))
        print("===== Step {step} End =====".format(step=step))