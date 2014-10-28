__author__ = 'e.kolpakov'


class BaseMessage:
    def __init__(self):
        pass


class KnowledgeMessage(BaseMessage):
    def __init__(self, fact):
        self._fact = fact

    @property
    def fact(self):
        return self._fact

