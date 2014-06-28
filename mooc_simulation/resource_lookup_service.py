__author__ = 'e.kolpakov'


class ResourceLookupService:
    def __init__(self, *args, **kwargs):
        self._access_privileges = dict()
        self._resources = None

        super(ResourceLookupService, self).__init__(*args, **kwargs)

    def _register_resources(self, resources):
        """ :type resources: list[agents.Resource] """
        self._resources = resources

    def grant_access(self, student, resource):
        """
        :type student: agents.Student
        :type resource: agents.Resource
        """
        if student.name not in self._access_privileges:
            self._access_privileges[student.name] = dict()
        self._access_privileges[student.name][resource.name] = True

    def check_access(self, student, resource):
        """
        :type student: agents.Student
        :type resource: agents.Resource
        :rtype: bool
        """
        if student.name in self._access_privileges:
            if resource.name in self._access_privileges[student.name]:
                return self._access_privileges[student.name][resource.name]
        return False

    def get_accessible_resources(self, student):
        """
        :type student: agents.Student
        :rtype: tuple[agents.Resource]
        """
        return tuple([resource for resource in self._resources if self.check_access(student, resource)])