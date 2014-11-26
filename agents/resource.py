import itertools

from lazy import lazy

from agents.base_agents import BaseAgent
from knowledge_representation.lesson_type import Lecture
from simulation.resource_access import ResourceAccessService


__author__ = 'e.kolpakov'


class Resource(BaseAgent):
    def __init__(self, name, lessons, *args, **kwargs):
        """
        :type name: str
        :type lessons: list[BaseLesson]
        """
        super(Resource, self).__init__(*args, **kwargs)
        self._name = name
        self._lessons = lessons

        self._resource_access_service = None

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @property
    def lessons(self):
        """
        :rtype: tuple[BaseLesson]
        """
        return tuple(self._lessons)

    @lazy
    def lectures(self):
        return tuple(lesson for lesson in self.lessons if isinstance(lesson, Lecture))

    @lazy
    def facts_to_study(self):
        return tuple(itertools.chain(*[lecture.facts for lecture in self.lectures]))

    @property
    def resource_access_service(self):
        """ :rtype: ResourceAccessService """
        return self._resource_access_service

    @resource_access_service.setter
    def resource_access_service(self, value):
        """
        :param value: ResourceAccessService
        """
        if not isinstance(value, ResourceAccessService):
            raise ValueError("expected ResourceAccessService instance, {0} given".format(value))
        self._resource_access_service = value

    def allow_access(self, student):
        return self.resource_access_service.check_access(student, self)
