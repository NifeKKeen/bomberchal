import globals
from pygame.locals import *

from entitites.bots.aggressive_bot import AggressiveBot
from entitites.bots.boss_bot import BossBot
from entitites.bots.wandering_bot import WanderingBot
from entitites.interfaces.BombSpawnable import BombSpawnable
from utils import paint_api, snapshot_api
from utils.helpers import rand, get_field_pos, get_tick_from_ms, calc_speed_per_time
from utils.interaction_api import is_clicked, is_pressed
from utils.paint_api import mount_rect
from utils.sound_api import play_music
from entitites.bonus import Bonus, bonus_types
from entitites.bots.original_bot import Bot, OriginalBot
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.obstacle import Obstacle
from entitites.player import Player, get_players
from pages.game import field_generator
from pages.navigation import navigate
from config import load_config

DEFAULT_FIELD = [
    [globals.VOID_CELL if rand(0, 100) < 50 else globals.U_OBSTACLE_CELL for j in range(20)] for i in range(20)
]

def setup_game(**kwargs):
    globals.rows = kwargs.get("rows", 23)
    globals.cols = kwargs.get("cols", 25)
    load_config()
    reset_game()
    for i in range(globals.cols):
        for j in range(globals.rows):
            mount_rect(  #region parameters
                image_path="assets/images/terrain/grass1.png",

                px_x=i * globals.CELL_SIZE, px_y=j * globals.CELL_SIZE,
                px_w = globals.CELL_SIZE, px_h = globals.CELL_SIZE,
                x=i, y=j,

                key = f"v-{i};{j}",
                layer=-1,
            )  #endregion

    if globals.game_mode == "default":
        play_music(globals.GAME_MUSIC_PATH1, .1, override=True)
    else:
        play_music(globals.GAME_MUSIC_PATH2, .5, override=True)

    control_keys = [
        (K_w, K_UP),
        (K_s, K_DOWN),
        (K_a, K_LEFT),
        (K_d, K_RIGHT),
        (globals.controls_players[0]["explosion_key"], globals.controls_players[1]["explosion_key"]),
        (K_1, K_KP1)
    ]

    for i in range(2):
        player = Player(  #region parameters
            speed=calc_speed_per_time(16, 100),
            lives=1,
            bomb_power=7,
            bomb_allowed=5,
            bomb_timer=get_tick_from_ms(3000),
            spread_type="bfs",
            character_skin_key=f"ch{[globals.skin_p1_id, globals.skin_p2_id][i]}",

            move_up_key=control_keys[0][i],
            move_down_key=control_keys[1][i],
            move_left_key=control_keys[2][i],
            move_right_key=control_keys[3][i],
            attack_key=control_keys[4][i],
            attack_func=Player.spawn_bomb,
            bonus_activation_key=control_keys[5][i],

            px_x=(1 if i == 0 else globals.cols - 1) * globals.CELL_SIZE,
            px_y=(1 if i == 0 else globals.rows - 1) * globals.CELL_SIZE,
            px_w=globals.PLAYER_CELL_SIZE,
            px_h=globals.PLAYER_CELL_SIZE,

            key=f"p-{i}",
        )  #endregion

    render_field()

    while len(globals.state_snapshots):
        globals.state_snapshots.pop().clear()
    globals.cur_state_spawned_sprites.clear()
    globals.cur_state_killed_sprites.clear()


def render_field(**kwargs):
    field = globals.field
    rows = globals.rows
    cols = globals.cols
    for x in range(cols):
        for y in range(rows):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                obstacle_sprite = Obstacle(  #region parameters
                    type=field[x][y],
                    seed=0,

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w = globals.CELL_SIZE, px_h = globals.CELL_SIZE,
                    x=x, y=y,

                    key = f"o-{x};{y}",
                )  #endregion

            elif field[x][y] == globals.D_OBSTACLE_CELL:
                obstacle_seed = rand(1, 3)

                obstacle_sprite = Obstacle(  #region parameters
                    type=field[x][y],
                    seed=obstacle_seed,

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w = globals.CELL_SIZE, px_h = globals.CELL_SIZE,
                    x=x, y=y,

                    key = f"o-{x};{y}",
                )  #endregion

            elif field[x][y] == globals.ORIGINAL_BOT_CELL:
                bot = OriginalBot(  #region parameters
                    speed=calc_speed_per_time(8, 100),
                    bomb_power=2,
                    bomb_countdown=get_tick_from_ms(1500),
                    spread_type="star",

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(0, 255, 0),

                    key = f"orig-bot-{x};{y}",
                )  #endregion

            elif field[x][y] == globals.WANDERING_BOT_CELL:
                bot = WanderingBot(  #region parameters
                    speed=calc_speed_per_time(12, 100),

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(0, 0, 255),

                    key = f"wand-bot-{x};{y}",
                )  #endregion

            elif field[x][y] == globals.AGGRESSIVE_BOT_CELL:
                bot = AggressiveBot(  #region parameters
                    speed=calc_speed_per_time(10, 100),
                    bomb_power=1,
                    bomb_countdown=get_tick_from_ms(3000),
                    #boredom_countdown=get_tick_from_ms(10000),
                    spread_type="star",

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(255, 0, 0),

                    key = f"aggro-bot-{x};{y}",
                )  #endregion

            elif field[x][y] == globals.BOSS_BOT_CELL:
                bot = BossBot(  #region parameters
                    lives=20,
                    speed=calc_speed_per_time(16, 100),
                    bomb_power=8,
                    bomb_allowed=1,
                    bomb_countdown=get_tick_from_ms(3500),
                    damage_countdown=get_tick_from_ms(500),
                    boredom_countdown=get_tick_from_ms(10000),
                    spread_type="bfs",

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    # px_w=globals.CELL_SIZE * 3, px_h=globals.CELL_SIZE * 3,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(255, 0, 0),

                    key = f"boss-bot-{x};{y}",
                )  #endregion

def reset_game():
    paint_api.reset_frame()
    globals.game_tick = 0
    globals.state_snapshots.clear()
    globals.field = field_generator.generate(globals.cols, globals.rows, globals.game_mode)
    globals.field_fire_state = [[0] * globals.rows for _ in range(globals.cols)]

def spawn_bonus(bonus_type = 0):
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
        bonus = Bonus(  #region parameters
            type=bonus_types()[bonus_type],

            px_x=bonus_x * globals.CELL_SIZE, px_y=bonus_y * globals.CELL_SIZE,
            px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
            x=bonus_x, y=bonus_y,
            color=[(123, 123, 0), (123, 0, 123), (0, 123, 123), (123, 0, 0)][bonus_type],

            key=f"bonus-{bonus_x};{bonus_y}",
        )  #endregion
        return

    for x in range(globals.cols):
        for y in range(globals.rows):
            collision = False
            for entity in globals.entities:
                if entity.x == bonus_x and entity.y == bonus_y:
                    collision = True
                    break
            if not collision:
                bonus = Bonus(  #region parameters
                    speed=0,
                    type=bonus_types()[bonus_type],

                    px_x=bonus_x * globals.CELL_SIZE, px_y=bonus_y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=bonus_x, y=bonus_y,
                    color=[(123, 123, 0), (123, 0, 123), (0, 123, 123), (0, 0, 0)][bonus_type],

                    key=f"bonus-{bonus_x};{bonus_y}",
                )  #endregion
                return

def handle_bonus_items_render():
    # 1, 2, ..., 0 for both players
    for i in range(1, 11):
        for player in range(2):
            paint_api.mount_text(  #region parameters
                px_x=(i - 0.75) * globals.CELL_SIZE,
                px_y=(globals.rows + player) * globals.CELL_SIZE,
                layer = globals.TEXT_LAYER,
                text=str(i % 10),
                font_size=30,
                color=(222, 222, 222),

                key=f"bonus_key-{i}-{player}",
            )  #endregion

    # rendering bonuses in inventory
    for player in list(get_players(globals.entities)):
        x = 0
        for bonus in player.get_bonus_instances():

            if bonus.activated:
                continue

            npx_x, npx_y = get_field_pos(x, globals.rows + (player.key[-1] == '1'))
            mount_rect(  #region parameters
                px_x=npx_x, px_y=npx_y,
                px_w=bonus.px_w, px_h=bonus.px_h,
                layer=globals.BASE_ENTITY_LAYER,

                color=bonus.color,
                image_path=bonus.image_path,

                key=f"inv-{player.key}-{bonus.key}",
                dynamic=True,
            )  #endregion

            x += 1

def game(**kwargs):
    is_setup = kwargs.get("is_setup", False)

    # if len(get_bots(globals.entities)) == 0 and len(get_players(globals.entities)) > 0:
    #     globals.game_mode = "bossfight"
    #     is_setup = True

    if is_setup:
        setup_game(**kwargs)
        return

    go_menu_button_sprite = paint_api.mount_rect(  #region parameters
        px_x=0, px_y=0,
        px_w=40, px_h=40,
        layer=globals.BUTTON_LAYER + globals.LAYER_SHIFT,

        key="go_menu"
    )  #endregion

    handle_bonus_items_render()

    if is_clicked(go_menu_button_sprite):
        navigate("menu")

    if is_pressed(K_t):
        globals.time_reversing_count_down = 2

    if globals.time_reversing_count_down:
        if globals.tick % globals.SNAPSHOT_CAPTURE_DELAY == 0:
            snapshot_api.restore_last_snapshot()
    else:
        if globals.tick % globals.SNAPSHOT_CAPTURE_DELAY == 0:
            snapshot_api.capture()

    globals.time_reversing_count_down = max(0, globals.time_reversing_count_down - 1)
    if globals.time_reversing_count_down:
        return

    if globals.game_tick % 400 == 0:
        spawn_bonus(rand(0, 4))

    if len(get_players(globals.entities)) == 0:
        bg_overlay = paint_api.mount_rect( #region parameters
            px_x=0, px_y=0,
            px_w=globals.cols * globals.CELL_SIZE, px_h=globals.rows * globals.CELL_SIZE,
            layer=globals.LAYER_SHIFT - 1,
            image_path="assets/images/backgrounds/overlay.png",
            key="bg_overlay"
        ) #endregion
        game_over_text = paint_api.mount_text( #region parameters
            px_x=globals.CENTER_X,
            px_y=globals.CENTER_Y - 100,
            layer=globals.TEXT_LAYER + globals.LAYER_SHIFT,
            align="center",
            text="Game over",
            font_size=50,
            color=(255, 0, 0),
            key="game_over_text",
        ) #endregion
        back_button_sprite = paint_api.mount_rect( #region parameters
            px_x=globals.CENTER_X,
            px_y=globals.CENTER_Y + 50,
            px_w=200,
            px_h=80,
            layer=globals.BUTTON_LAYER + globals.LAYER_SHIFT,
            align="center",
            image_path="assets/images/buttons/bar_button.png",
            key="game_over_back",
        ) #endregion
        back_pos = back_button_sprite.px_x, back_button_sprite.px_y
        back_button_shadow = paint_api.mount_text( #region parameters
            px_x=back_pos[0] + globals.SHADOW_OFFSET,
            px_y=back_pos[1] + globals.SHADOW_OFFSET,
            layer=globals.SHADOW_LAYER + globals.LAYER_SHIFT,
            align="center",
            text="Back",
            font_size=50,
            color=globals.SHADOW_COLOR,

            key="back_text_shadow",
        ) #endregion
        back_button_text = paint_api.mount_text( #region parameters
            px_x=back_pos[0],
            px_y=back_pos[1],
            layer=globals.TEXT_LAYER + globals.LAYER_SHIFT,
            align="center",
            text="Back",
            font_size=50,
            color=(255, 255, 255),
            key="game_over_back_text",
        ) # endregion

        if is_clicked(back_button_sprite):
            navigate("menu")
            return


    globals.game_tick += 1
    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        entity.add_tick()

        entity.cur_damage_countdown = max(entity.cur_damage_countdown - 1, 0)

        if isinstance(entity, BombSpawnable):
            entity.cur_bomb_countdown = max(entity.cur_bomb_countdown - 1, 0)
        if isinstance(entity, Controllable):
            entity.handle_event()
        if isinstance(entity, Bot):
            if isinstance(entity, AggressiveBot):
                entity.cur_boredom_countdown = max(entity.cur_boredom_countdown - 1, 0)
            entity.think()

    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        if isinstance(entity, Collidable):
            entity.handle_collision()
