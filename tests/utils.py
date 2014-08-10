__author__ = 'e.kolpakov'


def iterate_event_generator(generator, times=None):
    times_counter = times if times else 0
    try:
        while times is None or times_counter > 0:
            next(generator)
            times_counter -= 1
    except StopIteration:
            pass