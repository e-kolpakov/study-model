from output.output_collector import OutputCollector
from output.output_renders.console_output_render import ConsoleOutputRender
from output.output_specification.output_specification import OutputSpecification
from runner import Runner
from simulation_specification.resource_specification import ResourceSpecification
from simulation_specification.simulation_specification import SimulationSpecification
from simulation_specification.student_specification import StudentSpecification

__author__ = 'john'


def read_simulation_spec():
    """
    :rtype: SimulationSpecification
    """
    sim_spec = SimulationSpecification()
    sim_spec.course_competencies.extend(['algebra', 'calculus', 'differential diff_eq'])
    sim_spec.students.append(StudentSpecification("John", {'algebra': 0, 'calculus': 0, 'diff_eq': 0}, 'basic', 's1'))
    sim_spec.students.append(StudentSpecification("Jim", {'algebra': 0.2, 'calculus': 0, 'diff_eq': 0}, 'basic', 's2'))
    sim_spec.resources.append(
        ResourceSpecification("Resource1", {'algebra': 1.0, 'calculus': 0.2, 'diff_eq': 0}, 'basic', resource_id='r1')
    )
    sim_spec.resources.append(
        ResourceSpecification("Resource1", {'algebra': 0.0, 'calculus': 0.8, 'diff_eq': 1.0}, 'basic', resource_id='r2')
    )
    return sim_spec


def read_output_spec():
    """
    :rtype: OutputSpecification
    """
    return OutputSpecification()


if __name__ == "__main__":
    simulation_spec, output_spec = read_simulation_spec(), read_output_spec()

    runner = Runner(simulation_spec)
    output_collector = OutputCollector(output_spec)
    output_collector.register_consumers()

    runner.initialize()
    runner.run()

    output_render = ConsoleOutputRender()
    output_render.render(output_collector.get_results())
