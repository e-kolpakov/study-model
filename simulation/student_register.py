from collections import defaultdict
import itertools

__author__ = 'e.kolpakov'


class StudentRegister:
    def __init__(self):
        self._student_lookup = defaultdict(list)

    def add_student(self, key, student):
        self._student_lookup[key].append(student)

    def get_students(self, key):
        return self._student_lookup[key]

    def get_student(self, key, idx=0):
        students = self._student_lookup[key]
        return students[idx] if len(students) > idx else None

    def get_all(self):
        return itertools.chain(*self._student_lookup.values())