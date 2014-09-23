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

    def activate(self, length):
        entered = self.env.now
        self._logger.debug("Student {name} study session of length {length} started at {time}".format(
            name=self._student.name, time=self.env.now, length=length
        ))

        choose_resource = self._student.behavior.resource_choice.choose_resource
        study_resource = self._student.study_resource
        get_accessible_resources = self._student.resource_lookup_service.get_accessible_resources
        stop_participation = self._student.behavior.stop_participation.stop_participation
        get_remaining_time = lambda now: entered + length - now

        def get_loop_parameters():
            res = get_accessible_resources(self._student)
            stop = stop_participation(self._student, self._student.curriculum, res)
            time = get_remaining_time(self.env.now)
            return time, res, stop

        remaining_time, resources, stop_participation = get_loop_parameters()
        while remaining_time > 0 and not stop_participation and resources:
            resource_to_study = choose_resource(self._student, self._student.curriculum, resources, remaining_time)
            self._logger.info(
                "Student {0}: resource {1} chosen at {2}".format(self._student, resource_to_study, self.env.now)
            )
            yield from study_resource(resource_to_study)
            remaining_time, resources, stop_participation = get_loop_parameters()

        if stop_participation:
            self._student.stop_participation()