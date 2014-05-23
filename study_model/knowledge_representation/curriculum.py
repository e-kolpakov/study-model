__author__ = 'e.kolpakov'


class Curriculum:
    def __init__(self):
        self._competency_index = {}
        self._fact_index = {}
        self._competency_fact_index = {}

    def register_competency(self, competency, overwrite=False):
        """
        Registers competency with curriculum.
        Updates code->competency, code->fact and fact->competency indices.
        :param competency: Competency
        """
        if competency.code in self._competency_index and not overwrite:
            raise ValueError("Competency {0} already registered".format(competency))

        self._competency_index[competency.code] = competency

        for fact in competency.facts:
            if fact.code in self._fact_index and not overwrite:
                raise ValueError("Fact {0} already registered".format(fact))
            self._fact_index[fact.code] = fact
            self._competency_fact_index[fact.code] = competency

    def find_competency(self, competency_code):
        """
        Finds competency by code
        :param competency_code: str
        :rtype: Competency
        """
        return self._competency_index.get(competency_code, None)

    def find_fact(self, fact_code):
        """
        Finds fact by code
        :param fact_code: str
        :rtype: Fact
        """
        return self._fact_index.get(fact_code, None)

    def find_competency_by_fact(self, fact):
        """
        Finds fact by code
        :param fact: Fact
        :rtype: Competency
        """
        return self._competency_fact_index.get(fact.code, None)

    def all_competencies(self):
        return self._competency_index.values()