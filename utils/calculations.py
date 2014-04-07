__author__ = 'john'


def get_competency_delta(new, old):
    """
    :type new: dict[Competency, double]
    :type old: dict[Competency, double]
    """
    return {
        competency: max(new_value - old.get(competency, 0), 0)
        for competency, new_value in new.items()
    }
