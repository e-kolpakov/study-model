import random
from agents.student.messages import FactMessage

__author__ = 'e.kolpakov'


class BaseSendMessagesBehavior:
    def __init__(self):
        pass

    def choose_students(self, student):
        pass

    def generate_messages(self, from_student, to_student):
        pass

    def send_messages(self, student):
        students = self.choose_students(student)
        return ((to_student, self.generate_messages(student, to_student)) for to_student in students)


class ChooseAllStudentsMixin:
    def choose_students(self, student):
        return student.known_students


class ChooseRandomStudentsMixin:
    def choose_students(self, student):
        known_students = student.known_students
        student_number = random.randint(1, len(known_students))
        return random.sample(known_students, student_number)


class RandomFactMessagesMixin:
    def generate_messages(self, from_student, to_student):
        fact = random.choice(from_student.knowledge)
        return FactMessage(fact),


class RandomFactToAllStudentsInteractionBehavior(ChooseAllStudentsMixin, RandomFactMessagesMixin,
                                                 BaseSendMessagesBehavior):
    pass


class RandomFactToRandomStudentsInteractionBehavior(ChooseRandomStudentsMixin, RandomFactMessagesMixin,
                                                    BaseSendMessagesBehavior):
    pass
