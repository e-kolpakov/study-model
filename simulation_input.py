from agents.behaviors.student.behavior_group import BehaviorGroup
from agents.behaviors.student.knowledge_acquisition import AllDependenciesAcquisitionBehavior
from agents.behaviors.student.resource_choice import RationalResourceChoiceBehavior
from study_model.competency import Competency
from agents.resource import Resource
from agents.student import Student
from simulation_engine.simulation_input import SimulationInput
from study_model.curriculum import Curriculum
from study_model.fact import Fact, ResourceFact

__author__ = 'e.kolpakov'


def get_simulation_input():
    """
    :rtype: SimulationInput
    """
    sim_input = SimulationInput()
    curriculum = build_curriculum()

    sim_input.curriculum = curriculum
    sim_input.students.extend(build_students(curriculum))
    sim_input.resources.extend(build_resources(curriculum))

    return sim_input


def build_curriculum():
    curriculum = Curriculum()
    alg_fact_codes = ['Sum', "Sub", "Mul", "Div"]
    calc_fact_codes = ["Lim", "Int", "Der"]
    diff_eq_fact_codes = ["LinearDE", "SquareDE", "MultipleVarDE"]
    trig_fact_codes = ["Sin", "Cos", "Tan", "Ctg", "SinCos"]
    alg = Competency('algebra', [Fact(code) for code in alg_fact_codes])
    calc = Competency("calculus", [Fact(code, alg_fact_codes) for code in calc_fact_codes])
    diff_eq = Competency("diff_eq", [Fact(code, alg_fact_codes + calc_fact_codes) for code in diff_eq_fact_codes])
    trig = Competency("trigonometry", [Fact(code, alg_fact_codes) for code in trig_fact_codes])

    curriculum.register_competency(alg)
    curriculum.register_competency(calc)
    curriculum.register_competency(diff_eq)
    curriculum.register_competency(trig)

    return curriculum


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


def build_students(curriculum):
    rational_behavior = BehaviorGroup()
    rational_behavior.resource_choice = RationalResourceChoiceBehavior()
    rational_behavior.knowledge_acquisition = AllDependenciesAcquisitionBehavior()

    return [
        Student("John", [], rational_behavior, agent_id='s1'),
        Student("Jim", [], rational_behavior, agent_id='s2')
    ]


