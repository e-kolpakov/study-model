import logging

import simpy


__author__ = 'e.kolpakov'


class BaseStudentActivity:
    def __init__(self, student, length=None, env=None):
        """:type: Student"""
        self._student = student
        self._env = env if env else student.env
        self._length = length
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def env(self):
        return self._env

    @property
    def length(self):
        return self._length

    def run(self, **kwargs):
        raise NotImplemented

    def cancel(self):
        pass


class IdleActivity(BaseStudentActivity):
    def run(self, parameters=None):
        self._logger.debug("{student} idle session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=self._length
        ))
        yield self.env.timeout(self._length)


class StudySessionActivity(BaseStudentActivity):
    PARAMETER_INTERRUPTIBLE = 'interruptable'

    def run(self, **kwargs):
        entered = self.env.now
        self._logger.debug("{student} study session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=self._length
        ))

        interruptible = kwargs.get(self.PARAMETER_INTERRUPTIBLE, False)

        study_until = entered + self._length

        choose_resource = self._student.behavior.resource_choice.choose_resource
        study_resource = self._student.study_resource
        get_accessible_resources = self._student.get_accessible_resources
        stop_participation = self._student.behavior.stop_participation.stop_participation

        def get_loop_parameters():
            res = get_accessible_resources()
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
    def run(self, **kwargs):
        entered = self.env.now
        interact_until = entered + self._length

        yield from self._student.process_messages(until=interact_until)
        yield from self._student.send_messages(until=interact_until)


class PassExamActivity(BaseStudentActivity):
    def run(self, **kwargs):
        entered = self.env.now
        complete_before = entered + self._length

        exam = self._student.choose_exam()

        if not exam:
            return

        exam_feedback = yield from exam.take(self._student, complete_before)
        self._student.get_feedback(exam, exam_feedback)