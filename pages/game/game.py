import globals
from pygame.locals import *

from entitites.bots.aggressive_bot import AggressiveBot
from entitites.bots.boss_bot import BossBot
from entitites.bots.wandering_bot import WanderingBot
from utils import paint_api
from utils.helpers import rand, get_field_pos, get_tick_from_ms
from utils.interaction_api import is_clicked, is_pressed, is_pressed_once
from utils.paint_api import mount_rect
from utils.sound_api import play_music
from entitites.bonus import Bonus, bonus_types, get_bonuses
from entitites.bots.original_bot import Bot, OriginalBot
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.obstacle import Obstacle
from entitites.player import Player, get_players
from pages.game import field_generator
from pages.navigation import navigate

DEFAULT_FIELD = [
    [globals.VOID_CELL if rand(0, 100) < 50 else globals.U_OBSTACLE_CELL for j in range(20)] for i in range(20)
]
control_keys = []

def setup_game(**kwargs):
    for i in range(30):
        for j in range(30):
            mount_rect(
                px_x=i * globals.cell_size, px_y=j * globals.cell_size,
                px_w = globals.cell_size, px_h = globals.cell_size,
                x=i, y=j,
                key = f"v-{i};{j}",
                color=(64, 64, 64),
                entity_group=globals.entities,
                layer=-1,
                image_path="assets/images/terrain/grass1.png"
            )

    play_music(globals.game_music_path, .1, override=True)

    globals.rows = kwargs.get("rows", 23)
    globals.cols = kwargs.get("cols", 25)
    globals.field = kwargs.get("field", field_generator.generate(globals.cols, globals.rows, globals.game_mode))
    globals.field_fire_state = kwargs.get("field_fired",
        [[0] * globals.rows for _ in range(globals.cols)]
    )

    global control_keys
    control_keys = [
        (K_w, K_UP),
        (K_s, K_DOWN),
        (K_a, K_LEFT),
        (K_d, K_RIGHT),
        (globals.controls_players[0]["explosion_key"], globals.controls_players[1]["explosion_key"]),
        (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0),
        (K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP0)
    ]

    for i in range(2):
        rnd = rand(192, 256)
        player = Player(
            speed=2,
            lives=3,
            bomb_power=7,
            bomb_allowed=5,
            bomb_timer=get_tick_from_ms(3000),
            spread_type="star",

            move_up_key=control_keys[0][i],
            move_down_key=control_keys[1][i],
            move_left_key=control_keys[2][i],
            move_right_key=control_keys[3][i],
            attack_key=control_keys[4][i],
            attack_func=Player.spawn_bomb,

            px_x=(1 if i == 0 else globals.cols - 1) * globals.cell_size, px_y=(1 if i == 0 else globals.rows - 1) * globals.cell_size,
            px_w=globals.player_cell_size, px_h=globals.player_cell_size,

            key=f"p-{i}",
            layer=260,
            color=(0, rnd / 2, rnd),
            entity_group=globals.entities,
        )

    render_field()

def render_field(**kwargs):
    field = globals.field
    rows = globals.rows
    cols = globals.cols
    for x in range(cols):
        for y in range(rows):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                obstacle_sprite = Obstacle(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w = globals.cell_size, px_h = globals.cell_size,
                    x=x, y=y,
                    key = f"o-{x};{y}",
                    color=(64, 64, 64),
                    type=field[x][y],
                    entity_group=globals.entities
                )


            elif field[x][y] == globals.D_OBSTACLE_CELL:
                obstacle_sprite = Obstacle(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w = globals.cell_size, px_h = globals.cell_size,
                    x=x, y=y,
                    key = f"o-{x};{y}",
                    color=(255, 255, 64),
                    type=field[x][y],
                    entity_group=globals.entities
                )

            elif field[x][y] == globals.ORIGINAL_BOT_CELL:
                bot = OriginalBot(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    x=x, y=y,
                    speed=1,
                    color=(0, 255, 0),
                    bomb_countdown=get_tick_from_ms(500),
                    layer=256,
                    bomb_power=2,
                    entity_group=globals.entities,
                    key = f"orig-bot-{x};{y}",
                )

            elif field[x][y] == globals.WANDERING_BOT_CELL:
                bot = WanderingBot(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    x=x, y=y,
                    speed=1,
                    color=(0, 0, 255),
                    layer=256,
                    entity_group=globals.entities,
                    key = f"wand-bot-{x};{y}",
                )

            elif field[x][y] == globals.AGGRESSIVE_BOT_CELL:
                bot = AggressiveBot(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    x=x, y=y,
                    speed=1,
                    color=(255, 0, 0),
                    bomb_countdown=get_tick_from_ms(500),
                    layer=256,
                    bomb_power=4,
                    entity_group=globals.entities,
                    key = f"aggro-bot-{x};{y}",
                )

            elif field[x][y] == globals.BOSS_BOT_CELL:
                bot = BossBot(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    # px_w=globals.cell_size * 3, px_h=globals.cell_size * 3,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    x=x, y=y,
                    speed=2,
                    color=(255, 0, 0),
                    layer=256,
                    entity_group=globals.entities,
                    bomb_countdown=get_tick_from_ms(500 + 3000),
                    bomb_power=8,
                    bomb_allowed=1,
                    damage_countdown=get_tick_from_ms(500),
                    lives=20,
                    key = f"boss-bot-{x};{y}",
                )

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
        bonus = Bonus(
            px_x=bonus_x * globals.cell_size, px_y=bonus_y * globals.cell_size,
            px_w=globals.cell_size, px_h=globals.cell_size,
            speed = 0,
            type=bonus_types()[bonus_type],
            x=bonus_x, y=bonus_y,
            color=[(123, 123, 0), (123, 0, 123), (0, 123, 123), (123, 0, 0)][bonus_type],
            layer=251,
            entity_group=globals.entities,
            key=f"bonus-{bonus_x};{bonus_y}"
        )
        return

    for x in range(globals.cols):
        for y in range(globals.rows):
            collision = False
            for entity in globals.entities:
                if entity.x == bonus_x and entity.y == bonus_y:
                    collision = True
                    break
            if not collision:
                bonus = Bonus(
                    px_x=bonus_x * globals.cell_size, px_y=bonus_y * globals.cell_size,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    speed=0,
                    type=bonus_types()[bonus_type],
                    x=bonus_x, y=bonus_y,
                    color=[(123, 123, 0), (123, 0, 123), (0, 123, 123), (0, 0, 0)][bonus_type],
                    layer=251,
                    entity_group=globals.entities,
                    key=f"bonus-{bonus_x};{bonus_y}"
                )
                return

def handle_bonuses():
    # 1, 2, ..., 0 for both players
    for i in range(1, 11):
        for player in range(2):
            paint_api.mount_text(
                px_x=(i - 0.75) * globals.cell_size,
                px_y=(globals.rows + player) * globals.cell_size,
                key=f"bonus_key-{i}-{player}",
                text=str(i % 10),
                font_size=30,
                color=(222, 222, 222),
                layer = 300
            )

    # handling keys
    for i in range(1, 11):
        for player in range(2):
            global control_keys
            if is_pressed_once(control_keys[5 + player][i - 1]):
                for entity in list(globals.entities):
                    if not isinstance(entity, Player):
                        continue
                    if entity.key[-1] != str(player):
                        continue

                    # Correct player
                    x = 0
                    for bonus in entity.bonuses:
                        if not bonus.mounted:
                            continue
                        x += 1
                        if x == i:
                            bonus.activate()
                            break
    # rendering bonuses
    for entity in list(globals.entities):
        if not isinstance(entity, Player):
            continue
        # Player
        x = 0
        for bonus in entity.bonuses:
            if not bonus.mounted:
                continue
            bonus.x = x
            bonus.y = globals.rows + (entity.key[-1] == '1')
            x += 1

            bonus.px_x, bonus.px_y = get_field_pos(bonus.x, bonus.y)
            bonus.set_px(bonus.px_x, bonus.px_y)

def game(**kwargs):
    is_setup = kwargs.get("is_setup", False)
    if is_setup:
        setup_game(**kwargs)
        return

    go_menu_button_sprite = paint_api.mount_rect(px_x=0, px_y=0, px_w=40, px_h=40, layer=300, key="go_menu")

    if is_clicked(go_menu_button_sprite):
        navigate("menu")

    if globals.tick % 10 == 0:
        spawn_bonus(rand(0, 4))

    if len(get_players(globals.entities)) == 0:
        raise Exception("You lost")

    handle_bonuses()

    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        if isinstance(entity, Controllable):
            entity.handle_event()
        if isinstance(entity, Bot):
            entity.think()
        if isinstance(entity, Bonus):
            entity.update()
        if isinstance(entity, Collidable):
            entity.handle_collision()