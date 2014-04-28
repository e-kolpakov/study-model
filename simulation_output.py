import operator

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
        for student, delta in result.competencies_delta.items():
            deltas = [(competency, value) for competency, value in delta.items()]
            deltas.sort(key=operator.itemgetter(0))
            delta_str = ", ".join(
                "{code}: {value}".format(code=competency, value=value) for competency, value in deltas)
            print("Student {name}: {delta}".format(name=student, delta=delta_str))
        print("===== Step {step} End =====".format(step=step))