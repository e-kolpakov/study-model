from abc import ABCMeta, abstractmethod
import logging


__author__ = 'e.kolpakov'


class BaseStudentActivity(metaclass=ABCMeta):
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

    @abstractmethod
    def run(self, **kwargs):
        raise NotImplemented

    def cancel(self):
        pass

    can_skip_if_not_required_by_goal = False

    def __str__(self):
        return type(self).__name__

    def __unicode__(self):
        return self.__str__()
    
    def __repr__(self):
        return super(BaseStudentActivity, self).__repr__()


class IdleActivity(BaseStudentActivity):
    def run(self, parameters=None):
        self._logger.debug("{student} idle session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=self._length
        ))
        yield self.env.timeout(self._length)


class StudySessionActivity(BaseStudentActivity):
    can_skip_if_not_required_by_goal = True

    def run(self, **kwargs):
        entered = self.env.now
        self._logger.debug("{student} study session of length {length} started at {time}".format(
            student=self._student, time=self.env.now, length=self._length
        ))

        study_until = entered + self._length

        choose_resource = self._student.behavior.resource_choice.choose_resource
        study_resource = self._student.study_resource
        get_accessible_resources = self._student.get_accessible_resources

        remaining_time, resources = (study_until - self.env.now), list(get_accessible_resources())
        while remaining_time > 0 and resources:
            resource_to_study = choose_resource(self._student, self._student.curriculum, resources, remaining_time)
            if resource_to_study is None:
                break
            self._logger.info("{0}: resource {1} chosen at {2}".format(self._student, resource_to_study, self.env.now))
            study_event = self.env.process(study_resource(resource_to_study, study_until))
            completed = yield study_event
            if not completed:
                break
            remaining_time, resources = (study_until - self.env.now), list(get_accessible_resources())


class PeerStudentInteractionActivity(BaseStudentActivity):
    def run(self, **kwargs):
        entered = self.env.now
        interact_until = entered + self._length

        yield from self._student.process_messages(until=interact_until)
        yield from self._student.send_messages(until=interact_until)


class PassExamActivity(BaseStudentActivity):
    can_skip_if_not_required_by_goal = True

    def run(self, **kwargs):
        entered = self.env.now
        complete_before = entered + self._length

        exam = self._student.choose_exam(complete_before)

        if not exam:
            return

        self._logger.info(
            "{student} attempts {exam} at {now}".format(student=self._student, exam=exam, now=self.env.now)
        )

        exam_feedback = yield from exam.take(self._student, complete_before)
        self._student.accept_feedback(exam=exam, exam_feedback=exam_feedback)
        self._logger.info("{student} {exam} attempt finished with grade {grade} at {now}".format(
            student=self._student, exam=exam, now=self.env.now, grade=exam_feedback.grade
        ))