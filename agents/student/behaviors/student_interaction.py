import random
import itertools

from agents.student.messages import FactMessage, ResourceMessage

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

    def generate_messages(self, from_student, to_student, **kwargs):
        """
        :param Student from_student: student sending messages
        :param Student to_student: recipient student
        :param kwargs: keyword arguments
        :rtype: itertools.Iterable[BaseMessage]
        """
        return tuple()

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
    def generate_messages(self, from_student, to_student, **kwargs):
        """
        :param Student from_student: student sending messages
        :param Student to_student: recipient student
        :param kwargs: keyword arguments
        :rtype: itertools.Iterable[BaseMessage]
        """
        if not from_student.knowledge:
            return

        fact = random.sample(from_student.knowledge, 1)[0]
        yield FactMessage(fact)
        yield from super(RandomFactMessagesMixin, self).generate_messages(from_student, to_student, **kwargs)


class RandomResourceMessagesMixin:
    def generate_message(self, from_student, to_student, **kwargs):
        """
        :param Student from_student: student sending messages
        :param Student to_student: recipient student
        :param kwargs: keyword arguments
        :rtype: itertools.Iterable[BaseMessage]
        """
        available_resources = from_student.known_resources
        if not available_resources:
            return

        resource = random.sample(available_resources)
        yield ResourceMessage(resource)
        yield from super(RandomResourceMessagesMixin, self).generate_message(from_student, to_student, **kwargs)



class RandomFactToAllStudentsInteractionBehavior(ChooseAllStudentsMixin, RandomFactMessagesMixin,
                                                 RandomResourceMessagesMixin, BaseSendMessagesBehavior):
    pass


class RandomFactToRandomStudentsInteractionBehavior(ChooseRandomStudentsMixin, RandomFactMessagesMixin,
                                                    RandomResourceMessagesMixin, BaseSendMessagesBehavior):
    pass
