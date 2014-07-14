__author__ = 'e.kolpakov'


class BaseStopParticipationBehavior:
    def __init__(self):
        pass

    def stop_participation(self, student, curriculum, available_resources):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: list[Resource] | tuple[Resource]
        :rtype: bool
        """
        pass


class CourseCompleteStopParticipationBehavior(BaseStopParticipationBehavior):
    def stop_participation(self, student, curriculum, available_resources):
        """
        :param student: Student
        :param curriculum: Curriculum
        :param available_resources: list[Resource] | tuple[Resource]
        :rtype: bool
        """
        return all(competency.is_mastered(student.knowledge) for competency in curriculum.all_competencies())
