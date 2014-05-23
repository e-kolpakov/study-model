__author__ = 'john'


def output_results(results):
    """
    :type results: dict[int, SimulationResult]
    """
    for step, result in results.items():
        print("======= Step {step} =======".format(step=step))
        for resource, usage in result.resource_usage.items():
            print("Resource {name} used {times} times".format(name=resource, times=usage))
        # print("=== Snapshots ===")
        # for student, snapshot in result.competencies_snapshot.items():
        #     print("Student {name}: {snapshot}".format(name=student, snapshot=snapshot))
        print("===== Delta =====")
        for student, new_knowledge in result.new_knowledge.items():
            delta_str = ", ".join(list(map(str, new_knowledge)))
            print("Student {name}: {delta}".format(name=student, delta=delta_str))
        print("===== Step {step} End =====".format(step=step))