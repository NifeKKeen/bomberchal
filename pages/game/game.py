import globals
from pygame.locals import *

from entitites.bot import get_bots
from entitites.bots.aggressive_bot import AggressiveBot
from entitites.bots.boss_bot import BossBot
from entitites.bots.wandering_bot import WanderingBot
from utils import paint_api
from utils.helpers import rand, get_field_pos, get_tick_from_ms
from utils.interaction_api import is_clicked, is_pressed_once
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
from pages.menu.customization import load_config

DEFAULT_FIELD = [
    [globals.VOID_CELL if rand(0, 100) < 50 else globals.U_OBSTACLE_CELL for j in range(20)] for i in range(20)
]

def setup_game(**kwargs):
    load_config()
    for i in range(30):
        for j in range(30):
            mount_rect(  #region parameters
                image_path="assets/images/terrain/grass1.png",

                px_x=i * globals.CELL_SIZE, px_y=j * globals.CELL_SIZE,
                px_w = globals.CELL_SIZE, px_h = globals.CELL_SIZE,
                x=i, y=j,

                key = f"v-{i};{j}",
                layer=-1,
                entity_group=globals.entities,
            )  #endregion

    if globals.game_mode == "default":
        play_music(globals.GAME_MUSIC_PATH1, .1, override=True)
    else:
        play_music(globals.GAME_MUSIC_PATH2, .5, override=True)


    globals.rows = kwargs.get("rows", 23)
    globals.cols = kwargs.get("cols", 25)
    globals.field = kwargs.get("field", field_generator.generate(globals.cols, globals.rows, globals.game_mode))
    globals.field_fire_state = kwargs.get("field_fired",
        [[0] * globals.rows for _ in range(globals.cols)]
    )

    control_keys = [
        (K_w, K_UP),
        (K_s, K_DOWN),
        (K_a, K_LEFT),
        (K_d, K_RIGHT),
        (globals.controls_players[0]["explosion_key"], globals.controls_players[1]["explosion_key"]),
        (K_1, K_KP1)
    ]

    for i in range(2):
        rnd = rand(192, 256)
        player = Player(  #region parameters
            speed=2,
            lives=3,
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
            color=(0, rnd / 2, rnd),
            entity_group=globals.entities,
        )  #endregion

    render_field()

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
                    entity_group=globals.entities,
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
                    entity_group=globals.entities,
                )  #endregion

            elif field[x][y] == globals.ORIGINAL_BOT_CELL:
                bot = OriginalBot(  #region parameters
                    speed=1,
                    bomb_power=2,
                    bomb_countdown=get_tick_from_ms(1500),

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(0, 255, 0),

                    key = f"orig-bot-{x};{y}",
                    entity_group=globals.entities,
                )  #endregion

            elif field[x][y] == globals.WANDERING_BOT_CELL:
                bot = WanderingBot(  #region parameters
                    speed=1,

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(0, 0, 255),

                    key = f"wand-bot-{x};{y}",
                    entity_group=globals.entities,
                )  #endregion

            elif field[x][y] == globals.AGGRESSIVE_BOT_CELL:
                bot = AggressiveBot(  #region parameters
                    speed=1,
                    bomb_power=4,
                    bomb_countdown=get_tick_from_ms(3000),

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(255, 0, 0),

                    key = f"aggro-bot-{x};{y}",
                    entity_group=globals.entities,
                )  #endregion

            elif field[x][y] == globals.BOSS_BOT_CELL:
                bot = BossBot(  #region parameters
                    lives=20,
                    speed=2,
                    bomb_power=8,
                    bomb_allowed=1,
                    bomb_countdown=get_tick_from_ms(3500),
                    damage_countdown=get_tick_from_ms(500),

                    px_x=x * globals.CELL_SIZE, px_y=y * globals.CELL_SIZE,
                    # px_w=globals.CELL_SIZE * 3, px_h=globals.CELL_SIZE * 3,
                    px_w=globals.CELL_SIZE, px_h=globals.CELL_SIZE,
                    x=x, y=y,
                    color=(255, 0, 0),

                    key = f"boss-bot-{x};{y}",
                    entity_group=globals.entities,
                )  #endregion

def reset_game():
    globals.entities.clear()

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
            entity_group=globals.entities,
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
                    entity_group=globals.entities,
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
        for bonus in player.bonuses:
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

    go_menu_button_sprite = paint_api.mount_rect(  #region parameters
        px_x=0, px_y=0,
        px_w=40, px_h=40,
        layer=globals.BUTTON_LAYER + globals.LAYER_SHIFT,

        key="go_menu"
    )  #endregion

    if is_clicked(go_menu_button_sprite):
        navigate("menu")

    if globals.tick % 400 == 0:
        spawn_bonus(rand(0, 4))

    if len(get_players(globals.entities)) == 0:
        raise Exception("You lost")

    handle_bonus_items_render()

    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        if isinstance(entity, Controllable):
            entity.handle_event()
        if isinstance(entity, Bot):
            entity.think()
        if isinstance(entity, Collidable):
            entity.handle_collision()
