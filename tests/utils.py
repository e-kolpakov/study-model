import types

__author__ = 'e.kolpakov'


def iterate_event_generator(generator, times=None, recursive=True):
    times_counter = times if times else 0
    result = []
    try:
        while times is None or times_counter > 0:
            next_item = next(generator)
            result.append(next_item)
            if isinstance(next_item, types.GeneratorType) and recursive:
                iterate_event_generator(next_item, recursive)
            times_counter -= 1
    except StopIteration:
            pass
    return result