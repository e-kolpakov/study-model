__author__ = 'e.kolpakov'


class BaseMessage:
    def __init__(self):
        pass

    def process(self, student, until=None):
        pass


class FactMessage(BaseMessage):
    def __init__(self, fact):
        super(FactMessage, self).__init__()
        self._fact = fact

    @property
    def fact(self):
        return self._fact

    def process(self, student, until=None):
        student.study_fact(self._fact, until)

