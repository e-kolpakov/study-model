__author__ = 'john'


class OutputSpecification(object):
    def __init__(self):
        self._observables = None
        """ :type: list[Observable]"""

    @property
    def observables(self):
        """
        :rtype: list[Observable]
        """
        return self._observables

    @observables.setter
    def observables(self, value):
        """
        :type value: list[Observable]
        """
        self._observables = value
