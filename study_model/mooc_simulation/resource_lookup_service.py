from study_model.agents.resource import Resource

__author__ = 'e.kolpakov'


class ResourceLookupService:
    def __init__(self, *args, **kwargs):
        self._access_privileges = dict()
        self._resources = None

        super(ResourceLookupService, self).__init__(*args, **kwargs)

    def _register_resources(self, resources):
        """
        :type resources: list[Resource]
        """
        self._resources = resources

    def grant_access(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        """
        if student.name not in self._access_privileges:
            self._access_privileges[student.name] = dict()
        self._access_privileges[student.name][resource.name] = True

    def check_access(self, student, resource):
        """
        :type student: Student
        :type resource: Resource
        :rtype: bool
        """
        if student.name in self._access_privileges:
            if resource.name in self._access_privileges[student.name]:
                return self._access_privileges[student.name][resource.name]
        return False

    def get_accessible_resources(self, student):
        """
        :type student: Student
        :rtype: tuple[Resource]
        """
        return tuple([resource for resource in self._resources if self.check_access(student, resource)])