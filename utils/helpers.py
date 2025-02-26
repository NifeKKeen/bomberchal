import random, globals


def get_ms_from_tick(tick):
    return tick * 1000 / globals.FPS

def get_tick_from_ms(ms):
    return (ms * globals.FPS) // 1000

def rand(l, r):
    # random number between [l, r)
    return random.randint(l, r - 1)

def get_field_pos(x, y):
    px_x = x * globals.cell_size
    px_y = y * globals.cell_size
    #print(x, y, px_x, px_y, "GET FIELD POS")
    return px_x, px_y


def get_pos(px_x, px_y):
    x = int(px_x + globals.cell_size * 0.5) // globals.cell_size
    y = int(px_y + globals.cell_size * 0.5) // globals.cell_size
    #print(px_x, px_y, x, y, "GET COORD POS")
    return x, y
