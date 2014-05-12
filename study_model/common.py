__author__ = 'john'


def get_available_facts(facts, known_facts, curriculum):
    """
    :param facts: set[Fact]
    :param known_facts: frozenset[Fact]
    :param curriculum: Curriculum
    :rtype: set[Fact]
    """
    competencies = []
    for fact in facts:
        competency = curriculum.find_competency_by_fact(fact)
        if competency not in competencies:
            competencies.append(competency)

    new, current = known_facts, known_facts
    while new:
        current |= new
        new = {
            fact
            for competency in competencies if competency.is_mastered(current)
            for fact in competency.facts if fact in facts
        }
    return current
