__author__ = 'john'


class BaseResourceChoiceBehavior:
    def __init__(self):
        pass

    def choose_resource(self, student, available_resources):
        """
        :type student: Student
        :type available_resources: list[Resource]
        :rtype: Resource
        """
        raise NotImplemented
