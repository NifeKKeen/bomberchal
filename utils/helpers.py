import math
import random, globals


def get_ms_from_tick(tick):
    return (tick * 1000) / globals.FPS

def get_tick_from_ms(ms):
    return (ms * globals.FPS) // 1000

def rand(l, r):
    # random number between [l, r)
    return random.randint(l, r - 1)

def get_field_pos(x, y):
    px_x = x * globals.cell_size
    px_y = y * globals.cell_size
    return px_x, px_y

def get_pos(px_x, px_y):
    x = int(px_x + globals.cell_size * 0.5) // globals.cell_size
    y = int(px_y + globals.cell_size * 0.5) // globals.cell_size
    return x, y

def get_pos_upper_left(px_x, px_y):
    x = int(px_x) // globals.cell_size
    y = int(px_y) // globals.cell_size
    return x, y

def in_valid_range(i, j, cols, rows):
    return 0 <= i < cols and 0 <= j < rows

def get_texture_type(stage_textures, sub_seed=0, ratio = 0):
    if math.isnan(ratio) or ratio * len(stage_textures[sub_seed]) >= len(stage_textures[sub_seed]):
        return stage_textures[sub_seed][0]
    return stage_textures[sub_seed][len(stage_textures[sub_seed]) - max(1, int(ratio * len(stage_textures[sub_seed])))]
