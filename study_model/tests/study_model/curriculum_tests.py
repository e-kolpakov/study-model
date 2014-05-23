import unittest
from study_model.knowledge_representation import Competency, Fact

from study_model.knowledge_representation.curriculum import Curriculum


__author__ = 'e.kolpakov'


class CurriculumTests(unittest.TestCase):
    def setUp(self):
        self.curriculum = Curriculum()

    def test_empty_curriculum_all_lookups_return_none(self):
        self.assertIsNone(self.curriculum.find_competency("qwe"))
        self.assertIsNone(self.curriculum.find_fact("qwe"))
        self.assertIsNone(self.curriculum.find_competency_by_fact(Fact("qwe")))

    def test_register_competency_can_lookup_by_code(self):
        comp1 = Competency('qwe', [])
        comp2 = Competency('zxc', [])
        self.curriculum.register_competency(comp1)
        self.curriculum.register_competency(comp2)

        self.assertEqual(self.curriculum.find_competency('qwe'), comp1)
        self.assertEqual(self.curriculum.find_competency('zxc'), comp2)

    def test_register_competency_can_lookup_fact_by_code(self):
        facts = [Fact("A"), Fact("B"), Fact("C"), Fact("D")]
        comp = Competency("Competency", facts)
        self.curriculum.register_competency(comp)

        self.assertEqual(self.curriculum.find_fact("A"), Fact("A"))
        self.assertEqual(self.curriculum.find_fact("B"), Fact("B"))
        self.assertEqual(self.curriculum.find_fact("C"), Fact("C"))
        self.assertEqual(self.curriculum.find_fact("D"), Fact("D"))

        self.assertIsNone(self.curriculum.find_fact("Z"))

    def test_register_competency_can_lookup_competency_by_fact(self):
        comp1 = Competency("Competency1", [Fact("A"), Fact("B")])
        comp2 = Competency("Competency2", [Fact("C"), Fact("D"), Fact("E")])

        self.curriculum.register_competency(comp1)
        self.curriculum.register_competency(comp2)

        self.assertEqual(self.curriculum.find_competency_by_fact(Fact("A")), comp1)
        self.assertEqual(self.curriculum.find_competency_by_fact(Fact("B")), comp1)

        self.assertEqual(self.curriculum.find_competency_by_fact(Fact("C")), comp2)
        self.assertEqual(self.curriculum.find_competency_by_fact(Fact("D")), comp2)
        self.assertEqual(self.curriculum.find_competency_by_fact(Fact("E")), comp2)