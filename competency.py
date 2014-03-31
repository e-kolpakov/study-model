__author__ = 'john'


class Competency:
    def __init__(self, code, dependencies=None):
        """
        :type code: str
        :type dependencies: list[str]
        """
        self._code = code
        self._dependencies = dependencies if dependencies else tuple()

    @property
    def code(self):
        """
        :rtype: str
        """
        return self._code

    @property
    def dependencies(self):
        """
        :rtype: tuple[str]
        """
        return tuple(self._dependencies)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    def __repr__(self):
        return "{code} <= {dependencies}".format(code=self.code, dependencies=self.dependencies)

    def __eq__(self, other):
        return self.code == other.code and set(self.dependencies) == set(other.dependencies)

    def __lt__(self, other):
        return self.code in other.dependencies

    def __gt__(self, other):
        return other.code in self.dependencies

    def __hash__(self):
        return hash((self.code, self.dependencies))
