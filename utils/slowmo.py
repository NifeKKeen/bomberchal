import globals


def can_tick():
    return globals.time_slowdown_count_down % 4 == 0
