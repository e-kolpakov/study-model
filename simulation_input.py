from agents.behaviors import RationalResourceChoiceBehavior, AllPrerequisitesRequiredKnowledgeAcquisitionBehavior
from agents.behaviors.student.behavior_group import BehaviorGroup
from agents.behaviors.student.resource_choice import RandomResourceChoiceBehavior
from study_model.competency import Competency
from agents.resource import Resource
from agents.student import Student
from simulation_engine.simulation_input import SimulationInput
from study_model.curriculum import Curriculum
from study_model.fact import Fact, ResourceFact

__author__ = 'john'


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
    alg = Competency('algebra', [Fact('Sum'), Fact("Sub"), Fact("Mul"), Fact("Div")])
    calc = Competency("calculus", [Fact("Lim"), Fact("Int"), Fact("Der")], ['algebra'])
    diff_eq = Competency("diff_eq", [Fact("LinearDE"), Fact("SquareDE"), Fact("MultipleVarDE")], ['algebra', 'calculus'])
    trig = Competency("trigonometry", [Fact("Sin"), Fact("Cos"), Fact("Tan"), Fact("Ctg"), Fact("SinCos")])

    curriculum.register_competency(alg)
    curriculum.register_competency(calc)
    curriculum.register_competency(diff_eq)
    curriculum.register_competency(trig)

    return curriculum


def build_resources(curriculum):
    to_resource_facts = lambda fact_codes: [ResourceFact(curriculum.find_fact(code)) for code in fact_codes]
    return [
        Resource("Resource1", to_resource_facts(['Sum', "Sub", "Mul", "Div", "Lim"]), None, agent_id='r1'),
        Resource("Resource2", to_resource_facts(['Int', "Der", "LinearDE", "SquareDE", "MultipleVarDE"]), None, agent_id='r2'),
        Resource("Resource3", to_resource_facts(curriculum.find_competency("trigonometry").facts), None, agent_id='r3')
    ]


def build_students(curriculum):
    rational_behavior = BehaviorGroup()
    rational_behavior.resource_choice = RationalResourceChoiceBehavior()
    rational_behavior.knowledge_acquisition = AllPrerequisitesRequiredKnowledgeAcquisitionBehavior()

    return [
        Student("John", [], rational_behavior, agent_id='s1'),
        Student("Jim", [], rational_behavior, agent_id='s2')
    ]


