__author__ = 'e.kolpakov'


class BaseMessage:
    def __init__(self):
        pass

    def process(self, student, until=None):
        pass

    def time_to_send(self, student):
        pass


class FactMessage(BaseMessage):
    COMPLEXITY_REDUCTION_FACTOR = 5

    def __init__(self, fact):
        super(FactMessage, self).__init__()
        self._fact = fact

    @property
    def fact(self):
        return self._fact

    def process(self, student, until=None):
        yield from student.study_fact(self._fact, until)

    def time_to_send(self, student):
        return self._fact.complexity / student.skill / self.COMPLEXITY_REDUCTION_FACTOR

    def __repr__(self):
        return "FactMessage ({id}): {fact}".format(id=id(self), fact=self._fact)

