import unittest

from knowledge_representation import Competency, Fact, Curriculum

__author__ = 'e.kolpakov'


class CurriculumTests(unittest.TestCase):
    def setUp(self):
        self.curriculum = Curriculum()

    def test_empty_curriculum_all_lookups_return_none(self):
        self.assertIsNone(self.curriculum.find_competency("qwe"))
        self.assertIsNone(self.curriculum.find_fact("qwe"))

    def test_register_competency_can_lookup_by_code(self):
        comp1 = Competency('qwe', [])
        comp2 = Competency('zxc', [])
        self.curriculum.register_competency(comp1)
        self.curriculum.register_competency(comp2)

        self.assertEqual(self.curriculum.find_competency('qwe'), comp1)
        self.assertEqual(self.curriculum.find_competency('zxc'), comp2)

    def test_register_fact_can_lookup_fact_by_code(self):
        for fact in [Fact("A"), Fact("B"), Fact("C"), Fact("D")]:
            self.curriculum.register_fact(fact)

        self.assertEqual(self.curriculum.find_fact("A"), Fact("A"))
        self.assertEqual(self.curriculum.find_fact("B"), Fact("B"))
        self.assertEqual(self.curriculum.find_fact("C"), Fact("C"))
        self.assertEqual(self.curriculum.find_fact("D"), Fact("D"))

        self.assertIsNone(self.curriculum.find_fact("Z"))