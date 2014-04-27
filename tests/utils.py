__author__ = 'john'


def compare_dicts(d1, d2, comparer=None):
    """
    :type d1: dict
    :type d2: dict
    """
    actual_comparer = comparer if comparer else lambda x, y: x == y
    if d1.keys() != d2.keys():
        raise AssertionError("Keys do not match: {0} != {1}".format(d1.keys(), d2.keys()))

    for key in d1.keys():
        d1val = d1[key]
        d2val = d2[key]
        actual_comparer(d1val, d2val)
