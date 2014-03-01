from output_renders.output_render_base import OutputRenderBase

__author__ = 'john'


class ConsoleOutputRender(OutputRenderBase):
    def render(self, results):
        """
        :param SimulationResult results: simulation result object
        """
        print("="*10 + " SIMULATION RESULT START " + "="*10)
        for result in results.results:
            print("{key} {timestamp}: {value}".format(key=result.key, timestamp=result.timestamp, value=result.value))
        print("="*11 + " SIMULATION RESULT END " + "="*11)