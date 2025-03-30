import math, random, globals


def get_ms_from_tick(tick):
    return (tick * 1000) / globals.FPS


def get_tick_from_ms(ms):
    return (ms * globals.FPS + 999) // 1000  # ceiling


def rand(l, r):
    # random number between [l, r)
    return random.randint(l, r - 1)


def calc_speed_per_time(pixels, ms):
    return (pixels + get_tick_from_ms(ms) - 1) // get_tick_from_ms(ms)  # ceiling


def get_field_pos(x, y):
    px_x = x * globals.CELL_SIZE
    px_y = y * globals.CELL_SIZE
    return px_x, px_y


def get_pos(px_x, px_y):
    x = int(px_x + globals.CELL_SIZE * 0.5) // globals.CELL_SIZE
    y = int(px_y + globals.CELL_SIZE * 0.5) // globals.CELL_SIZE
    return x, y


def get_pos_upper_left(px_x, px_y):
    x = int(px_x) // globals.CELL_SIZE
    y = int(px_y) // globals.CELL_SIZE
    return x, y


def in_valid_range(i, j, cols, rows):
    return 0 <= i < cols and 0 <= j < rows


def get_texture_type(stage_textures, sub_seed=0, ratio = 0):
    if math.isnan(ratio) or ratio * len(stage_textures[sub_seed]) >= len(stage_textures[sub_seed]):
        return stage_textures[sub_seed][0]
    return stage_textures[sub_seed][len(stage_textures[sub_seed]) - max(1, int(ratio * len(stage_textures[sub_seed])))]


def players_sum_of_scores(scores):
    from entitites.entity import is_entity_key
    from entitites.player import PLAYER_KEY

    res = 0
    for key, score in scores.items():
        if is_entity_key(PLAYER_KEY, key):
            res += score

    return res
