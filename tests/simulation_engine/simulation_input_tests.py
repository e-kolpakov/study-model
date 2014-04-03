import unittest

from agents.behaviors.student.behavior_group import BehaviorGroup
from agents.student import Student
from agents.competency import Competency
from simulation_engine.simulation_input import SimulationInput


class SimulationInputTests(unittest.TestCase):
    def test_students_zero_knwoledge_for_each_missing_competency(self):
        sim_input = SimulationInput()

        A = Competency('A')
        B = Competency('B')
        C = Competency('C')
        sim_input.competencies.extend([A, B, C])

        student1 = Student("student1", {}, BehaviorGroup())
        student2 = Student("student2", {A: 0.1}, BehaviorGroup())
        student3 = Student("student3", {A: 0.1, B: 0.2, C: 0.3}, BehaviorGroup())

        sim_input.students.append(student1)
        sim_input.students.append(student2)
        sim_input.students.append(student3)

        sim_input.prepare()

        self.assertSequenceEqual(student1.competencies, {A: 0.0, B: 0.0, C: 0.0})
        self.assertSequenceEqual(student2.competencies, {A: 0.1, B: 0.0, C: 0.0})
        self.assertSequenceEqual(student3.competencies, {A: 0.1, B: 0.2, C: 0.3})


