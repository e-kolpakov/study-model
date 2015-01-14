import logging

__author__ = 'e.kolpakov'


class ResourceRosterMixin:
    def __init__(self, *args, **kwargs):
        self._known_resources = set()
        self._logger = getattr(self, '_logger', None)

    def add_resource(self, resource):
        if resource in self._known_resources:
            self._logger.debug("{self} already knows about resource {resource}".format(self=self, resource=resource))
        self._logger.debug("{self} adds resource {resource}".format(self=self, resource=resource))
        self._known_resources.add(resource)

    def forget_resource(self, resource):
        self._known_resources.remove(resource)

    @property
    def known_resources(self):
        return frozenset(self._known_resources)

    @property
    def logger(self):
        if not self._logger:
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger


class ResourceAccessService:
    def __init__(self, *args, **kwargs):
        self._access_privileges = dict()
        self._resources = None

        super(ResourceAccessService, self).__init__(*args, **kwargs)

    def _register_resources(self, resources):
        """ :type resources: list[agents.Resource] """
        self._resources = resources

    def grant_access(self, student, resource):
        """
        :type student: agents.student.Student
        :type resource: agents.resource.Resource
        """
        if student.name not in self._access_privileges:
            self._access_privileges[student.name] = dict()
        self._access_privileges[student.name][resource.name] = True

    def check_access(self, student, resource):
        """
        :type student: agents.student.Student
        :type resource: agents.resource.Resource
        :rtype: bool
        """
        if student.name in self._access_privileges:
            if resource.name in self._access_privileges[student.name]:
                return self._access_privileges[student.name][resource.name]
        return False

    def get_accessible_resources(self, student):
        """
        :type student: agents.student.Student
        :rtype: tuple[agents.resource.Resource]
        """
        return tuple([resource for resource in self._resources if self.check_access(student, resource)])