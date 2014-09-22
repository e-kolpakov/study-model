import logging

__author__ = 'e.kolpakov'


class BaseStudentActivity:
    def __init__(self):
        pass


class IdleStudentActivity(BaseStudentActivity):
    def __init__(self):
        super(IdleStudentActivity, self).__init__()

    def activate(self, student, length):
        yield student.env.timeout(length)


class StudySessionStudentActivity(BaseStudentActivity):
    def __init__(self):
        super(StudySessionStudentActivity, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    def activate(self, student, length, get_resources_callback, choose_resource_callback):
        resources = get_resources_callback()
        entered_session = student.env.now
        self._logger.debug("Student {name} study session of length {length} started at {time}".format(
            name=student.name, time=student.env.now, length=length
        ))

        while student.env.now - entered_session < length and not student.check_stop_participation(resources):
            self._logger.debug("Choosing a resource to study at {time}".format(time=student.env.now))
            resource_to_study = choose_resource_callback(resources)
            self._logger.info("Student {name}({id}): resource {resource_name}({resource_id}) chosen at {time}".format(
                name=student.name, id=student.agent_id,
                resource_name=resource_to_study.name, resource_id=resource_to_study.agent_id,
                time=student.env.now
            ))

            yield student.env.process(student.study_resource(resource_to_study))