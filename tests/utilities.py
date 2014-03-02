__author__ = 'john'
from collections import Counter


def unordered_equal(collection1, collection2):
    """
    :rtype: bool
    """
    return Counter(collection1) == Counter(collection2)
