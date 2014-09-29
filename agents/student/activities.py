import logging

__author__ = 'e.kolpakov'


class BaseStudentActivity:
    def __init__(self, student):
        """:type: Student"""
        self._student = student

    @property
    def env(self):
        return self._student.env


class IdleActivity(BaseStudentActivity):
    def __init__(self, student):
        super(IdleActivity, self).__init__(student)
        self._logger = logging.getLogger(self.__class__.__name__)

    def activate(self, length):
        self._logger.debug("{student} idle session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=length
        ))
        yield self.env.timeout(length)


class StudySessionActivity(BaseStudentActivity):
    def __init__(self, student):
        super(StudySessionActivity, self).__init__(student)
        self._logger = logging.getLogger(self.__class__.__name__)

    def activate(self, length):
        entered = self.env.now
        self._logger.debug("{student} study session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=length
        ))

        study_until = entered + length

        choose_resource = self._student.behavior.resource_choice.choose_resource
        study_resource = self._student.study_resource
        get_accessible_resources = self._student.resource_lookup_service.get_accessible_resources
        stop_participation = self._student.behavior.stop_participation.stop_participation

        def get_loop_parameters():
            res = get_accessible_resources(self._student)
            stop = stop_participation(self._student, self._student.curriculum, res)
            time = study_until - self.env.now
            return time, res, stop

        remaining_time, resources, stop = get_loop_parameters()
        while remaining_time > 0 and not stop and resources:
            resource_to_study = choose_resource(self._student, self._student.curriculum, resources, remaining_time)
            self._logger.info(
                "{0}: resource {1} chosen at {2}".format(self._student, resource_to_study, self.env.now)
            )
            study_resourse = self.env.process(study_resource(resource_to_study, study_until))
            completed = yield study_resourse
            if not completed:
                break
            remaining_time, resources, stop = get_loop_parameters()

        if stop:
            self._student.stop_participation()


class StudentInteractionActivity(BaseStudentActivity):
    def __init__(self, student):
        super(StudentInteractionActivity, self).__init__(student)

    def activate(self, length):
        pass