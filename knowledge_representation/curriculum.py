import logging

__author__ = 'e.kolpakov'


class Curriculum:
    def __init__(self):
        self._competency_index = {}
        self._fact_index = {}
        self._lesson_index = {}

    def register_competency(self, competency):
        """
        Registers competency with curriculum.
        :param competency: Competency
        """
        self._register(competency, self._competency_index)

    def register_fact(self, fact):
        """
        Registers fact with curriculum
        :param fact: Fact
        :return: None
        """
        self._register(fact, self._fact_index)

    def register_lesson(self, lesson):
        """
        Registers lesson with curriculum
        :param Lesson lesson: Lesson to register
        :return: None
        """
        self._register(lesson, self._lesson_index)

    def find_competency(self, competency_code):
        """
        Finds competency by code
        :param competency_code: str
        :rtype: knowledge_representation.Competency
        """
        return self._find(competency_code, self._competency_index)

    def find_fact(self, fact_code):
        """
        Finds fact by code
        :param fact_code: str
        :rtype: knowledge_representation.Fact
        """
        return self._find(fact_code, self._fact_index)

    def find_lesson(self, lesson_code):
        """
        Finds lesson by code
        :param lesson_code: str
        :rtype: BaseLesson
        """
        return self._find(lesson_code, self._lesson_index)

    def all_competencies(self):
        return self._competency_index.values()

    def all_facts(self):
        return self._fact_index.values()

    def all_lessons(self):
        return self._lesson_index.values()

    @staticmethod
    def _register(entity, index, message="{0} already registered", code_selector=None):
        code_selector = code_selector if code_selector else lambda x: x.code
        code = code_selector(entity)
        if code in index:
            message = message.format(entity)
            logging.getLogger(__name__).warn(message)
            raise ValueError(message)

        index[code] = entity

    @staticmethod
    def _find(code, index, default=None):
        """
        :param str code: code to look up
        :param dict index: index to search
        :param object|None default: default value if object is not found
        :rtype: object
        """
        return index.get(code, default)


