import copy
import logging
import simpy

__author__ = 'e.kolpakov'


class BaseStudentActivity:
    def __init__(self, student):
        """:type: Student"""
        self._student = student

    @property
    def env(self):
        return self._student.env

    def activate(self, length, **kwargs):
        raise NotImplemented


class IdleActivity(BaseStudentActivity):
    def __init__(self, student):
        super(IdleActivity, self).__init__(student)
        self._logger = logging.getLogger(self.__class__.__name__)

    def activate(self, length, **kwargs):
        self._logger.debug("{student} idle session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=length
        ))
        yield self.env.timeout(length)


class StudySessionActivity(BaseStudentActivity):
    def __init__(self, student):
        super(StudySessionActivity, self).__init__(student)
        self._logger = logging.getLogger(self.__class__.__name__)

    def activate(self, length, **kwargs):
        entered = self.env.now
        self._logger.debug("{student} study session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=length
        ))

        interruptable = kwargs.get('interruptable', False)

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
            except simpy.Interrupt as i:
                if not interruptable:
                    yield study_event
                else:
                    study_event.interrupt(i.cause)
                    break

        if stop:
            self._student.stop_participation()


class SymmetricalHandshakeActivity(BaseStudentActivity):
    def __init__(self, student):
        super(SymmetricalHandshakeActivity, self).__init__(student)

    def activate(self, length, **kwargs):
        from agents.student import Student
        other_student = kwargs.get('other_student', None)
        next_activity_type = kwargs.get('next_activity_type', None)
        if other_student is None or not isinstance(other_student, Student):
            raise ValueError("Student instance expected, {0} given".format(type(other_student)))
        if next_activity_type is None or not isinstance(next_activity_type, BaseStudentActivity):
            raise ValueError("Activity type expected, {0} given".format(type(next_activity_type)))

        wait_until = self.env.now + length
        other_availability = other_student.get_next_conversation_availability()

        next_activity_parameters = copy.deepcopy(kwargs)
        del next_activity_parameters['other_student']
        del next_activity_parameters['next_activity_type']

        if other_availability > wait_until:
            return False

        yield self.env.timeout(other_availability - self.env.now)
        next_activity_length = 10  # TODO: determine session length collaboratively
        other_started = other_student.request_activity_start(next_activity_type, next_activity_length, **next_activity_parameters)
        started = self._student.request_activity_start(next_activity_type, next_activity_length, **next_activity_parameters)
        return other_started and started


class StudentInteractionActivity(BaseStudentActivity):
    def __init__(self, student):
        super(StudentInteractionActivity, self).__init__(student)

    def activate(self, length, **kwargs):
        pass