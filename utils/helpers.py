import random, globals


def get_ms_from_tick(tick):
    return tick * 1000 / globals.FPS

def rand(l ,r):
    # random number between [l, r)
    return random.randint(l, r - 1)
