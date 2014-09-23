import logging

__author__ = 'e.kolpakov'


class BaseStudentActivity:
    def __init__(self, student):
        """:type: Student"""
        self._student = student

    @property
    def env(self):
        return self._student.env


class IdleStudentActivity(BaseStudentActivity):
    def __init__(self, student):
        super(IdleStudentActivity, self).__init__(student)

    def activate(self, length):
        yield self.env.timeout(length)


class StudySessionStudentActivity(BaseStudentActivity):
    def __init__(self, student):
        super(StudySessionStudentActivity, self).__init__(student)
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def student_behaviors(self):
        return self._student.behavior

    def _choose_resource(self, available_resources):
        return self.student_behaviors.resource_choice.choose_resource(
            self._student, self._student.curriculum, available_resources
        )

    def activate(self, length):
        entered_session = self.env.now
        self._logger.debug("Student {name} study session of length {length} started at {time}".format(
            name=self._student.name, time=self.env.now, length=length
        ))

        resources = self._student.resource_lookup_service.get_accessible_resources(self._student)
        while self.env.now - entered_session < length and \
                not self._student.check_stop_participation(resources) \
                and resources:
            self._logger.debug("Choosing a resource to study at {time}".format(time=self.env.now))
            resource_to_study = self._choose_resource(resources)
            self._logger.info("Student {name}({id}): resource {resource_name}({resource_id}) chosen at {time}".format(
                name=self._student.name, id=self._student.agent_id,
                resource_name=resource_to_study.name, resource_id=resource_to_study.agent_id,
                time=self.env.now
            ))

            yield self._student.env.process(self._student.study_resource(resource_to_study))
            resources = self._student.resource_lookup_service.get_accessible_resources(self._student)