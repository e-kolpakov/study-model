import pytest

from knowledge_representation import Competency, Fact, Curriculum

__author__ = 'e.kolpakov'


class TestCurriculum:
    @pytest.fixture
    def curriculum(self):
        return Curriculum()

    def test_empty_curriculum_all_lookups_return_none(self, curriculum):
        assert curriculum.find_competency("qwe") is None
        assert curriculum.find_fact("qwe") is None

    def test_register_competency_can_lookup_by_code(self, curriculum):
        comp1 = Competency('qwe', [])
        comp2 = Competency('zxc', [])
        curriculum.register_competency(comp1)
        curriculum.register_competency(comp2)

        assert curriculum.find_competency('qwe') == comp1
        assert curriculum.find_competency('zxc') == comp2

    def test_register_fact_can_lookup_fact_by_code(self, curriculum):
        for fact in [Fact("A"), Fact("B"), Fact("C"), Fact("D")]:
            curriculum.register_fact(fact)

        assert curriculum.find_fact("A") == Fact("A")
        assert curriculum.find_fact("B") == Fact("B")
        assert curriculum.find_fact("C") == Fact("C")
        assert curriculum.find_fact("D") == Fact("D")

        assert curriculum.find_fact("Z") is None