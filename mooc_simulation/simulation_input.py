from itertools import chain

from study_model.behaviors.student.behavior_group import BehaviorGroup
from behaviors.student.knowledge_acquisition import AllDependenciesAcquisitionBehavior
from study_model.behaviors.student.resource_choice import RationalResourceChoiceBehavior, RandomResourceChoiceBehavior
from study_model.agents.resource import Resource
from study_model.agents.student import Student
from study_model.knowledge_representation.competency import Competency
from study_model.knowledge_representation.curriculum import Curriculum
from study_model.knowledge_representation.fact import Fact, ResourceFact

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
        """ :rtype: list[Student] """
        return self._students

    @property
    def resources(self):
        """ :rtype: list[Resource] """
        return self._resources

    @property
    def curriculum(self):
        """ :rtype: Curriculum """
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
        return SimulationInput(curriculum, self.build_resources(curriculum), self.build_students(curriculum))

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

        return curriculum

    @staticmethod
    def build_resources(curriculum):
        to_resource_facts = lambda fact_codes: [ResourceFact(curriculum.find_fact(code)) for code in fact_codes]
        return [
            Resource("Resource1", to_resource_facts(['Sum', "Sub", "Mul", "Div"]), None, agent_id='r1'),
            Resource("Resource2", to_resource_facts(['Lim', "Int"]), None, agent_id='r2'),
            Resource("Resource3", to_resource_facts(['Lim', 'Int', 'Der']), None, agent_id='r3'),
            Resource("Resource4", to_resource_facts(['Int', "Der", "LinearDE", "SquareDE", "MultipleVarDE"]), None,
                     agent_id='r4'),
            Resource("Resource5", to_resource_facts(["Sin", "Cos", "Tan", "Ctg", "SinCos"]), None, agent_id='r5'),
        ]

    @staticmethod
    def build_students(curriculum):
        rational_behavior = BehaviorGroup()
        rational_behavior.resource_choice = RationalResourceChoiceBehavior()
        rational_behavior.knowledge_acquisition = AllDependenciesAcquisitionBehavior()

        random_behavior = BehaviorGroup()
        random_behavior.resource_choice = RandomResourceChoiceBehavior()
        random_behavior.knowledge_acquisition = AllDependenciesAcquisitionBehavior()

        return [
            Student("John", [], rational_behavior, agent_id='s1'),
            Student("Jim", [], rational_behavior, agent_id='s2')
        ]