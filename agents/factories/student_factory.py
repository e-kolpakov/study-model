from agents.behaviors.factory import BehaviorFactory
from agents.behaviors.student import resource_choice
from agents.behaviors.student.behavior_group import BehaviorGroup
from agents.student import Student
from simulation_specification.student_specification import StudentSpecification

__author__ = 'john'


class StudentFactory(object):
    def __init__(self):
        self._behavior_factory = BehaviorFactory()

    def produce(self, student_spec, all_competencies=None):
        """
        :param StudentSpecification student_spec: Student specification
        """
        all_comp = all_competencies if all_competencies else []
        behavior_group = self._get_behavior_group(student_spec.behavior)
        student = Student(student_spec.student_name, student_spec.competencies,
                          agent_id=student_spec.agent_id, behavior=behavior_group)
        student.competencies.update(
            {competency: 0 for competency in all_comp if competency not in student.competencies})
        return student

    def _get_behavior_group(self, behaviors_spec):
        """
        : type behaviors_spec: dict[str, str]
        : rtype: BehaviorGroup
        """
        behavior_group = BehaviorGroup()
        if resource_choice.BEHAVIOR_TYPE in behaviors_spec:
            choice_behavior_key = behaviors_spec[resource_choice.BEHAVIOR_TYPE]
        else:
            choice_behavior_key = "Rational"
        choice_behavior = self._behavior_factory.create_behavior(resource_choice.BEHAVIOR_TYPE+"."+choice_behavior_key)
        behavior_group.resource_choice = choice_behavior
        return behavior_group
