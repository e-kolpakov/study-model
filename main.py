from output_collector import OutputCollector
from output_renders.console_output_render import ConsoleOutputRender
from runner import Runner

__author__ = 'john'


def read_simulation_spec():
    return {}


def read_output_spec():
    return {}


if __name__ == "__main__":
    simulation_spec, output_spec = read_simulation_spec(), read_output_spec()

    runner = Runner(simulation_spec)
    output_collector = OutputCollector(output_spec)
    output_collector.register_consumers()

    runner.initialize()
    runner.run()

    output_render = ConsoleOutputRender()
    output_render.render(output_collector.get_results())
