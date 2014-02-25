__author__ = 'john'

from src.agents.base_agent import BaseAgent


class Student(BaseAgent):
    def __init__(self, resource_locator):
        self._resource_locator = resource_locator