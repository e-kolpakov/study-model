__author__ = 'john'


class CompetencyLookupService:
    def __init__(self):
        self._competency_lookup = None

    def _build_competency_lookup(self, competencies):
        """
        :type competencies: list[Competency]
        """
        self._competency_lookup = {competency.code: competency for competency in competencies}
        """ :type: dict[str, Competency] """

    def get_competency(self, code):
        """
        :type code: str
        :rtype: Competency
        """
        return self._competency_lookup.get(code, None)