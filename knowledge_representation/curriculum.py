import logging

__author__ = 'e.kolpakov'


class Curriculum:
    def __init__(self):
        self._competency_index = {}
        self._fact_index = {}
        self._logger = logging.getLogger(__name__)

    def register_competency(self, competency):
        """
        Registers competency with curriculum.
        :param competency: Competency
        """
        if competency.code in self._competency_index:
            message = "Competency {0} already registered".format(competency)
            self._logger.warn(message)
            raise ValueError(message)

        self._competency_index[competency.code] = competency

    def register_fact(self, fact):
        """
        Registers fact with curriculum
        :param fact: Fact
        :return: None
        """
        if fact.code in self._fact_index:
            message = "Fact {0} already registered".format(fact)
            self._logger.warn(message)
            raise ValueError(message)
        self._fact_index[fact.code] = fact

    def find_competency(self, competency_code):
        """
        Finds competency by code
        :param competency_code: str
        :rtype: knowledge_representation.Competency
        """
        return self._competency_index.get(competency_code, None)

    def find_fact(self, fact_code):
        """
        Finds fact by code
        :param fact_code: str
        :rtype: knowledge_representation.Fact
        """
        return self._fact_index.get(fact_code, None)

    def all_competencies(self):
        return self._competency_index.values()

    def all_facts(self):
        return self._fact_index.values()
