__author__ = 'john'


class Fact:
    def __init__(self, code):
        self._code = code

    @property
    def code(self):
        return self._code

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return isinstance(other, Fact) and self.code == other.code

    def __str__(self):
        return "Fact [{0}]".format(self.code)

    def __repr__(self):
        return "Fact [{0}] (id: {1})".format(self.code, id(self))


class ResourceFact:
    def __init__(self, fact, *args, **kwargs):
        """
        :type fact: Fact
        """
        self._fact = fact

    @property
    def fact(self):
        """
        :rtype: Fact
        """
        return self._fact

    def __str__(self):
        return "ResourceFact [{0}]".format(self.fact.code)

    def __repr__(self):
        return "ResourceFact [{0}] (id: {1})".format(self.fact.code, id(self))

