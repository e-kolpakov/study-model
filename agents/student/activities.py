import copy
import logging
import simpy

__author__ = 'e.kolpakov'


class BaseStudentActivity:
    def __init__(self, student):
        """:type: Student"""
        self._student = student
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def env(self):
        return self._student.env

    def prepare(self, **kwargs):
        return {}

    def run(self, length, **kwargs):
        raise NotImplemented

    def cancel(self):
        pass


class IdleActivity(BaseStudentActivity):
    def __init__(self, student):
        super(IdleActivity, self).__init__(student)
        self._logger = logging.getLogger(self.__class__.__name__)

    def run(self, length, parameters=None):
        self._logger.debug("{student} idle session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=length
        ))
        yield self.env.timeout(length)


class StudySessionActivity(BaseStudentActivity):
    PARAMETER_INTERRUPTIBLE = 'interruptable'

    def __init__(self, student):
        super(StudySessionActivity, self).__init__(student)
        self._logger = logging.getLogger(self.__class__.__name__)

    def run(self, length, **kwargs):
        entered = self.env.now
        self._logger.debug("{student} study session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=length
        ))

        interruptible = kwargs.get(self.PARAMETER_INTERRUPTIBLE, False)

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
            self._logger.info("{0}: resource {1} chosen at {2}".format(self._student, resource_to_study, self.env.now))
            study_event = self.env.process(study_resource(resource_to_study, study_until))
            try:
                completed = yield study_event
                if not completed:
                    break
                remaining_time, resources, stop = get_loop_parameters()
            # TODO: not tested and not verified
            except simpy.Interrupt as i:
                if not interruptible:
                    yield study_event
                else:
                    study_event.interrupt(i.cause)
                    break

        if stop:
            self._student.stop_participation()


class PeerStudentInteractionActivity(BaseStudentActivity):
    PARAMETER_OTHER_STUDENT = 'other_student'
    PARAMETER_SKIP_HANDSHAKE = 'skip_handshake'

    def __init__(self, student):
        super(PeerStudentInteractionActivity, self).__init__(student)

    def _get_other_student(self, kwargs):
        from agents.student import Student
        other_student = kwargs.get(self.PARAMETER_OTHER_STUDENT, None)
        if other_student is None or not isinstance(other_student, Student):
            raise ValueError("Student instance expected, {0} given".format(type(other_student)))
        return other_student

    def prepare(self, **kwargs):
        other_student = self._get_other_student(kwargs)

        if not kwargs.get(self.PARAMETER_SKIP_HANDSHAKE, False):
            wait_until = self.env.now + kwargs.get('max_wait', 2)
            other_availability = other_student.get_next_conversation_availability()

            if other_availability > wait_until:
                return None

            yield self.env.timeout(other_availability - self.env.now)

        return True

    def run(self, length, **kwargs):
        other_student = self._get_other_student(kwargs)
        other_kwargs = {self.PARAMETER_OTHER_STUDENT: self._student, self.PARAMETER_SKIP_HANDSHAKE: True}
        started = other_student.request_activity_start(PeerStudentInteractionActivity, length, other_kwargs)

        if not started:
            self._logger.debug("{student2} refused {activity} with {student1}".format(
                student1=self._student, activity=self, student2=other_student
            ))
        self._logger.debug("Handshake successful between {student1} and {student2} for {activity}".format(
            student1=self._student, activity=self, student2=other_student
        ))
