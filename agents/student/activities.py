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
    def student_behavior(self):
        return self._student.behavior

    def _choose_resource(self, available_resources, remaining_time):
        return self.student_behavior.resource_choice.choose_resource(
            self._student, self._student.curriculum, available_resources, remaining_time
        )

    def _get_remaining_time(self, entered, length):
        return entered + length - self.env.now

    def _check_stop_participation(self, available_resources):
        return self.student_behavior.stop_participation.stop_participation(
            self._student, self._student.curriculum, available_resources
        )

    def activate(self, length):
        entered = self.env.now
        self._logger.debug("Student {name} study session of length {length} started at {time}".format(
            name=self._student.name, time=self.env.now, length=length
        ))

        def get_loop_parameters():
            res = self._student.resource_lookup_service.get_accessible_resources(self._student)
            stop = self._check_stop_participation(res)
            time = self._get_remaining_time(entered, length)
            return time, res, stop

        remaining_time, resources, stop_participation = get_loop_parameters()
        while remaining_time > 0 and not stop_participation and resources:
            self._logger.debug("Choosing a resource to study at {time}".format(time=self.env.now))
            resource_to_study = self._choose_resource(resources, remaining_time)
            self._logger.info("Student {name}({id}): resource {resource_name}({resource_id}) chosen at {time}".format(
                name=self._student.name, id=self._student.agent_id,
                resource_name=resource_to_study.name, resource_id=resource_to_study.agent_id,
                time=self.env.now
            ))

            yield self._student.env.process(self._student.study_resource(resource_to_study))
            remaining_time, resources, stop_participation = get_loop_parameters()

        if stop_participation:
            self._student.stop_participation()