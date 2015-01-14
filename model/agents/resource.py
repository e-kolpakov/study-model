import itertools

from model.agents.base_agents import BaseAgent
from model.knowledge_representation.lesson_type import Lecture, Exam
from model.simulation.resource_access import ResourceAccessService


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

    @property
    def lectures(self):
        return tuple(self._get_lessons_of_type(Lecture))

    @property
    def exams(self):
        return tuple(self._get_lessons_of_type(Exam))

    def _get_lessons_of_type(self, lesson_type):
        return (
            lesson
            for lesson in self.lessons
            if isinstance(lesson, lesson_type) and lesson.publish_at <= self.env.now
        )

    @property
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
