import random
from agents.student.messages import FactMessage

__author__ = 'e.kolpakov'


class BaseSendMessagesBehavior:
    def __init__(self):
        pass

    def choose_students(self, student):
        """
        :param Student student: sender
        :rtype: List[Student]
        """
        pass

    def generate_messages(self, from_student, to_student):
        pass

    def get_messages(self, student):
        """
        Gets messages to be sent
        :param Student student: sender
        :rtype: collections.Iterable[(Student, collections.Iterable[BaseMessage])]
        """
        students = self.choose_students(student)
        return ((to_student, self.generate_messages(student, to_student)) for to_student in students)


class ChooseAllStudentsMixin:
    def choose_students(self, student):
        return student.known_students


class ChooseRandomStudentsMixin:
    def choose_students(self, student):
        known_students = student.known_students
        if not known_students:
            return tuple()

        student_number = random.randint(1, len(known_students))
        try:
            return random.sample(known_students, student_number)
        except TypeError:
            raise


class RandomFactMessagesMixin:
    def generate_messages(self, from_student, to_student):
        if not from_student.knowledge:
            return tuple()

        fact = random.sample(from_student.knowledge, 1)[0]
        return FactMessage(fact),


class RandomFactToAllStudentsInteractionBehavior(ChooseAllStudentsMixin, RandomFactMessagesMixin,
                                                 BaseSendMessagesBehavior):
    pass


class RandomFactToRandomStudentsInteractionBehavior(ChooseRandomStudentsMixin, RandomFactMessagesMixin,
                                                    BaseSendMessagesBehavior):
    pass
