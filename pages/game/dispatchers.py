import globals

from pygame.locals import *
from entitites.entity import format_entity_key
from entitites.player import Player, PLAYER_KEY
from pages.menu.play import get_setup_data_value
from utils import paint_api
from utils.helpers import rand, get_tick_from_ms, calc_speed_per_time
from entitites.bonus import Bonus, BONUS_KEY, MAP_SEED_BONUS_TYPE
from entitites.bots.aggressive_bot import AggressiveBot, AGGRESSIVE_BOT_KEY
from entitites.bots.boss_bot import BossBot, BOSS_BOT_KEY
from entitites.bots.wandering_bot import WanderingBot, WANDERING_BOT_KEY
from entitites.bots.original_bot import OriginalBot, ORIGINAL_BOT_KEY
from entitites.obstacle import Obstacle, format_obstacle_key
from utils.paint_api import mount_rect


def build_field():
    for i in range(globals.cols):
        for j in range(globals.rows):
            mount_rect(  # region parameters
                image_path="assets/images/terrain/grass1.png",

                px_x=i * globals.CELL_SIZE, px_y=j * globals.CELL_SIZE,
                px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                x=i, y=j,

                key=f"v-{i};{j}",
                layer=-1,
            )  # endregion

    field = globals.field
    rows = globals.rows
    cols = globals.cols
    boxes_count = get_setup_data_value("boxes")
    bricks_count = get_setup_data_value("bricks")

    box_ratio = boxes_count / (boxes_count + bricks_count) if boxes_count + bricks_count != 0 else 0

    # ENVIRONMENT GENERATION --------------------------
    for x in range(cols):
        for y in range(rows):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                obstacle_sprite = Obstacle(  # region parameters
                    type=field[x][y],
                    seed=0,

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,

                    key=format_obstacle_key(0, f"{x};{y}"),
                )  # endregion

            elif field[x][y] == globals.D_OBSTACLE_CELL:
                obstacle_seed = 1 if rand(0, 1000000) < int(box_ratio * 1000000) else 2
                if obstacle_seed == 1 and boxes_count <= 0:
                    obstacle_seed = 2
                elif obstacle_seed == 2 and bricks_count <= 0:
                    obstacle_seed = 1
                if obstacle_seed == 1:
                    boxes_count -= 1
                if obstacle_seed == 2:
                    bricks_count -= 1

                obstacle_sprite = Obstacle(  # region parameters
                    type=field[x][y],
                    seed=obstacle_seed,

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,

                    key=format_obstacle_key(obstacle_seed, f"{x};{y}"),
                )  # endregion

            elif field[x][y] == globals.ORIGINAL_BOT_CELL:
                bot = OriginalBot(  # region parameters
                    speed=calc_speed_per_time(8, 100),
                    bomb_power=2,
                    bomb_countdown=get_tick_from_ms(1500),
                    spread_type="star",

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(0, 255, 0),

                    key=format_entity_key(ORIGINAL_BOT_KEY, f"{x};{y}"),
                )  # endregion

            elif field[x][y] == globals.WANDERING_BOT_CELL:
                bot = WanderingBot(  # region parameters
                    speed=calc_speed_per_time(12, 100),

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(0, 0, 255),

                    key=format_entity_key(WANDERING_BOT_KEY, f"{x};{y}"),
                )  # endregion

            elif field[x][y] == globals.AGGRESSIVE_BOT_CELL:
                bot = AggressiveBot(  # region parameters
                    speed=calc_speed_per_time(10, 100),
                    bomb_power=4,
                    bomb_countdown=get_tick_from_ms(3000),
                    spread_type="star",

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(255, 0, 0),

                    key=format_entity_key(AGGRESSIVE_BOT_KEY, f"{x};{y}"),
                )  # endregion

            elif field[x][y] == globals.BOSS_BOT_CELL:
                bot = BossBot(  # region parameters
                    lives=30,
                    speed=calc_speed_per_time(12, 100),
                    bomb_power=4,
                    bomb_allowed=1,
                    bomb_countdown=get_tick_from_ms(3500),
                    damage_countdown=get_tick_from_ms(500),
                    spread_type="bfs",

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    # px_w=globals.CELL_SIZE * 3, px_h=globals.CELL_SIZE * 3,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(255, 0, 0),

                    key=format_entity_key(BOSS_BOT_KEY, f"{x};{y}"),
                )  # endregion
    # -------------------------------------------------

    # PLAYERS GENERATION ------------------------------
    player_cnt = get_setup_data_value("players")
    if globals.game_mode == "duel":
        player_cnt = 2

    control_keys = [
        (K_w, K_UP, K_i),
        (K_s, K_DOWN, K_k),
        (K_a, K_LEFT, K_j),
        (K_d, K_RIGHT, K_l),
        (globals.controls_players[0]["explosion_key"], globals.controls_players[1]["explosion_key"], K_n),  # bomb spawn keys
        (K_1, K_KP1, K_8)  # bonus use keys
    ]

    for i in range(player_cnt):
        player = Player(  # region parameters
            speed=calc_speed_per_time(8, 100),
            lives=get_setup_data_value("lives"),
            bomb_power=2,
            bomb_allowed=2,
            bomb_timer=get_tick_from_ms(3000),
            spread_type="star",
            character_skin_key=f"ch{[globals.skin_p1_id, globals.skin_p2_id][i]}",
            # character_skin_key=f"ch{[globals.skin_p1_id, globals.skin_p2_id, globals.skin_p3_id][i]}",
            player_id=i + 1,

            move_up_key=control_keys[0][i],
            move_down_key=control_keys[1][i],
            move_left_key=control_keys[2][i],
            move_right_key=control_keys[3][i],
            attack_key=control_keys[4][i],
            attack_func=Player.spawn_bomb,
            bonus_activation_key=control_keys[5][i],

            px_x=(1 if i == 0 else globals.cols - 2) * globals.CELL_SIZE,
            px_y=(1 if i == 0 else globals.rows - 2) * globals.CELL_SIZE,
            px_w=globals.PLAYER_CELL_SIZE,
            px_h=globals.PLAYER_CELL_SIZE,

            key=format_entity_key(PLAYER_KEY, i + 1),
        )  # endregion

    # -------------------------------------------------


def spawn_bonus(bonus_seed=0):
    attempts = 0
    while True:
        bonus_x, bonus_y = rand(0, globals.cols), rand(0, globals.rows)

        collision = False
        for entity in globals.entities:
            if entity.x == bonus_x and entity.y == bonus_y:
                collision = True
                break
        if collision:
            attempts += 1
            if attempts > globals.cols * globals.rows:
                break
            continue

        # found position
        bonus = Bonus(  # region parameters
            type=MAP_SEED_BONUS_TYPE[bonus_seed],

            px_x=bonus_x * globals.CELL_SIZE, px_y=bonus_y * globals.CELL_SIZE,
            px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
            x=bonus_x, y=bonus_y,

            key=format_entity_key(BONUS_KEY, f"{bonus_x};{bonus_y}"),
        )  # endregion
        return

    for x in range(globals.cols):
        for y in range(globals.rows):
            collision = False
            for entity in globals.entities:
                if entity.x == bonus_x and entity.y == bonus_y:
                    collision = True
                    break
            if not collision:
                bonus = Bonus(  # region parameters
                    speed=0,
                    type=MAP_SEED_BONUS_TYPE[bonus_seed],

                    px_x=bonus_x * globals.CELL_SIZE, px_y=bonus_y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=bonus_x, y=bonus_y,
                    color=[(123, 123, 0), (123, 0, 123), (0, 123, 123), (0, 0, 0)][bonus_seed],

                    key=format_entity_key(BONUS_KEY, f"{bonus_x};{bonus_y}"),
                )  # endregion
                return


def reset_game():
    paint_api.reset_frame()
    globals.game_tick = 0
    globals.time_reversing_count_down = 0
    globals.time_slowdown_count_down = 0
    globals.scores.clear()
    globals.state_snapshots.clear()
    globals.cur_state_spawned_sprites.clear()
    globals.cur_state_killed_sprites.clear()
    globals.field = None
    globals.field_fire_state = None
    globals.field_free_state = None
    globals.field_weight = None
