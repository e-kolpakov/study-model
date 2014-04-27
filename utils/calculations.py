__author__ = 'john'


def add_competencies(old, new, new_only=True):
    result = {
        competency_code: min(value + old.get(competency_code, 0), 1.0)
        for competency_code, value in new.items()
    }
    if not new_only:
        result.update({
            competency_code: value
            for competency_code, value in old.items()
            if competency_code not in result
        })
    return result


def get_competency_delta(new, old, only_new=True):
    """
    :type new: dict[str, double]
    :type old: dict[str, double]
    """
    result = {
        competency: max(new_value - old.get(competency, 0), 0)
        for competency, new_value in new.items()
    }
    if not only_new:
        result.update({
            competency_code: 0
            for competency_code in old.keys()
            if competency_code not in result
        })
    return result
