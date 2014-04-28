from agents.behaviors import RationalResourceChoiceBehavior, AllPrerequisitesRequiredKnowledgeAcquisitionBehavior
from agents.behaviors.student.behavior_group import BehaviorGroup
from study_model.competency import Competency
from agents.resource import Resource
from agents.student import Student
from simulation_engine.simulation_input import SimulationInput

__author__ = 'john'


def get_simulation_input():
    """
    :rtype: SimulationInput
    """
    sim_input = SimulationInput()
    alg = Competency('algebra')
    calc = Competency('calculus', ['algebra'])
    diff_eq = Competency('diff_eq', ['algebra', 'calculus'])
    trigonometry = Competency('trigonometry', ['algebra'])
    sim_input.competencies.extend([alg, calc, diff_eq, trigonometry])

    zero_knowledge = {competency.code: 0 for competency in sim_input.competencies}

    rational_behavior = BehaviorGroup()
    rational_behavior.resource_choice = RationalResourceChoiceBehavior()
    rational_behavior.knowledge_acquisition = AllPrerequisitesRequiredKnowledgeAcquisitionBehavior()

    random_behavior = BehaviorGroup()
    random_behavior.resource_choice = RationalResourceChoiceBehavior()
    rational_behavior.knowledge_acquisition = AllPrerequisitesRequiredKnowledgeAcquisitionBehavior()

    sim_input.students.append(
        Student("John", zero_knowledge, rational_behavior, agent_id='s1'))
    sim_input.students.append(
        Student("Jim", zero_knowledge, rational_behavior, agent_id='s2'))
    sim_input.resources.append(
        Resource("Resource1", {'algebra': 1.0, 'calculus': 0.2, 'diff_eq': 0, 'trigonometry': 0}, 'basic',
                 agent_id='r1')
    )
    sim_input.resources.append(
        Resource("Resource2", {'algebra': 0.0, 'calculus': 0.8, 'diff_eq': 1.0, 'trigonometry': 0}, 'basic',
                 agent_id='r2')
    )
    sim_input.resources.append(
        Resource("Resource3", {'algebra': 0.0, 'calculus': 0.0, 'diff_eq': 0.0, 'trigonometry': 1}, 'basic',
                 agent_id='r3')
    )
    return sim_input