from itertools import chain

from model.agents.resource import Resource
from model.agents.student.goals import StudyCompetenciesGoal, PassExamGoal
from model.agents.student import GoalDrivenStudent, RationalStudent
from model.knowledge_representation.fact import Competency, Fact
from model.knowledge_representation.curriculum import Curriculum
from model.knowledge_representation.lesson_type import Lecture, Exam


__author__ = 'e.kolpakov'


def get_simulation_input():
    """
    :return: SimulationInput
    """
    return SimulationInputBuilder().build()


class SimulationInput:
    def __init__(self, curriculum, resources, students):
        self._students = students
        self._resources = resources
        self._curriculum = curriculum

    @property
    def students(self):
        """ :rtype: list[agents.student] """
        return self._students

    @property
    def resources(self):
        """ :rtype: list[agents.Resource] """
        return self._resources

    @property
    def curriculum(self):
        """ :rtype: knowledge_representation.Curriculum """
        return self._curriculum


class SimulationInputBuilder:
    alg_fact_codes = ['Sum', "Sub", "Mul", "Div"]
    calc_fact_codes = ["Lim", "Int", "Der"]
    diff_eq_fact_codes = ["LinearDE", "SquareDE", "MultipleVarDE"]
    trig_fact_codes = ["Sin", "Cos", "Tan", "Ctg", "SinCos"]

    def build(self):
        """
        Builds Simulation input
        :return: SimulationInput
        """
        curriculum = self.build_curriculum()
        resources = self.build_resources(curriculum)
        return SimulationInput(curriculum, resources, self.build_students(curriculum, resources))

    def build_curriculum(self):
        curriculum = Curriculum()

        alg_facts = [Fact(code) for code in self.alg_fact_codes]
        calc_facts = [Fact(code, self.alg_fact_codes) for code in self.calc_fact_codes]
        diff_eq_facts = [Fact(code, self.alg_fact_codes + self.calc_fact_codes) for code in self.diff_eq_fact_codes]
        trig_facts = [Fact(code, self.alg_fact_codes) for code in self.trig_fact_codes]

        all_facts = chain(alg_facts, calc_facts, diff_eq_facts, trig_facts)
        for fact in all_facts:
            curriculum.register_fact(fact)

        curriculum.register_competency(Competency('algebra', alg_facts))
        curriculum.register_competency(Competency("calculus", calc_facts))
        curriculum.register_competency(Competency("diff_eq", diff_eq_facts))
        curriculum.register_competency(Competency("trigonometry", trig_facts))

        curriculum.register_lesson(Lecture("algebra", facts=alg_facts, name="Algebra"))
        curriculum.register_lesson(Lecture("trigonometry", facts=trig_facts, name="Trigonometry"))
        curriculum.register_lesson(Lecture("calculus1", facts=calc_facts[:2], name="Calculus 1"))
        curriculum.register_lesson(Lecture("calculus2", facts=calc_facts[2:], name="Calculus 2"))
        curriculum.register_lesson(Lecture("diff_eq1", facts=diff_eq_facts[:2], name="Differential Equations 1"))
        curriculum.register_lesson(Lecture("diff_eq2", facts=diff_eq_facts[2:], name="Differential Equations 2"))

        curriculum.register_lesson(
            Exam("half_semester_exam", facts=alg_facts+trig_facts, weight=0.3, name="Half semester exam", publish_at=40)
        )
        curriculum.register_lesson(
            Exam("final_exam", facts=alg_facts+trig_facts, weight=0.7, name="Final exam", publish_at=80)
        )

        return curriculum

    @staticmethod
    def build_resources(curriculum):
        get_lessons = lambda *codes: [curriculum.find_lesson(code) for code in codes]
        return [
            Resource("Basic Math", get_lessons("algebra", "trigonometry", "half_semester_exam"), agent_id='r1'),
            Resource("Calculus", get_lessons("calculus1", "calculus2"), agent_id='r2'),
            Resource("Differential Equations", get_lessons("diff_eq1", "diff_eq2", "final_exam"), agent_id='r3')
        ]

    @staticmethod
    def build_students(curriculum, resources):
        student1 = GoalDrivenStudent("Andy", [], agent_id='s1', skill=2.0)
        student1.goals.extend((
            StudyCompetenciesGoal([curriculum.find_competency('diff_eq')]),
        ))
        student2 = GoalDrivenStudent("Ben", [], agent_id='s2', skill=1.0)
        student2.goals.extend((
            StudyCompetenciesGoal([curriculum.find_competency('diff_eq')], weight=1.0),
            PassExamGoal(curriculum.find_lesson('final_exam'), weight=0.5)
        ))
        student3 = RationalStudent("Charlie", [], agent_id='s3', skill=1.0)
        student1.meet(student2)
        student2.meet(student1)

        students = [student1, student2, student3]
        for student in students:
            for resource in resources:
                student.add_resource(resource)

        return students