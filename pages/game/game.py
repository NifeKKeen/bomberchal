import pygame.mixer

from entitites.bonus import Bonus, bonus_types
from entitites.interfaces.BotIntellect import BotIntellect
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.obstacle import Obstacle
from pages.game import field_generator
from utils import paint_api
from pygame.locals import *
from pages.navigation import navigate
from entitites.bot import Bot
from entitites.player import Player
from utils.helpers import rand
from utils.interaction_api import is_clicked
import globals

DEFAULT_FIELD = [
    [globals.VOID_CELL if rand(0, 100) < 50 else globals.U_OBSTACLE_CELL for j in range(20)] for i in range(20)
]

def setup_game(**kwargs):
    globals.current_music = globals.game_music_path
    pygame.mixer.music.load(globals.game_music_path)
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1)

    globals.cols = kwargs.get("cols", 21)
    globals.rows = kwargs.get("rows", 21)
    globals.field = kwargs.get("field", field_generator.generate(globals.rows, globals.cols))
    globals.field_fire_state = kwargs.get("field_fired",
        [[0] * globals.cols for _ in range(globals.rows)]
    )

    control_keys = [
        (K_w, K_UP),
        (K_s, K_DOWN),
        (K_a, K_LEFT),
        (K_d, K_RIGHT),
        (globals.controls_players[0]["explosion_key"], globals.controls_players[1]["explosion_key"])
    ]

    for i in range(2):
        rnd = rand(192, 256)
        player = Player(
            mounted=True,
            px_x=(1 if i == 0 else 19) * globals.cell_size, px_y=(1 if i == 0 else 19) * globals.cell_size,
            px_w=globals.player_cell_size, px_h=globals.player_cell_size,
            move_up_key=control_keys[0][i],
            move_down_key=control_keys[1][i],
            move_left_key=control_keys[2][i],
            move_right_key=control_keys[3][i],
            attack_key=control_keys[4][i],
            attack_func=Player.spawn_bomb,
            speed=2,
            color=(0, rnd / 2, rnd),
            bomb_power=7,
            bomb_allowed=5,
            layer=260,
            bomb_timer=3000,
            entity_group=globals.entities,
            key=f"p-{i}"
        )

    render_field()

def render_field(**kwargs):
    field = globals.field
    for i in field:
        print(i)
    cols = globals.cols
    rows = globals.rows
    for x in range(cols):
        for y in range(rows):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                obstacle_sprite = Obstacle(
                    mounted=True,
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
                    mounted=True,
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w = globals.cell_size, px_h = globals.cell_size,
                    x=x, y=y,
                    key = f"o-{x};{y}",
                    color=(255, 255, 64),
                    type=field[x][y],
                    entity_group=globals.entities
                )


            elif field[x][y] == globals.BOT_CELL:
                bot = Bot(
                    mounted=True,
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    #px_w=globals.player_cell_size, px_h=globals.player_cell_size,
                    x=x, y=y,
                    speed=1,
                    color=((13*x) % 256, (13*y) % 256 , 255 * ((x + y) % 2)),
                    layer=256,
                    entity_group=globals.entities,
                )

def reset_game():
    globals.entities.clear()

def spawn_bonus(bonus_type = "Speed"):
    while True:
        bonus_x, bonus_y = rand(0, globals.rows), rand(0, globals.cols)
        collision = False
        #print(len(globals.entities))
        for entity in globals.entities:
            if entity.x == bonus_x and entity.y == bonus_y:
                collision = True
                break
        if collision:
            continue
        # found position
        bonus = Bonus(
            mounted=True,
            px_x=bonus_x * globals.cell_size, px_y=bonus_y * globals.cell_size,
            px_w=globals.cell_size, px_h=globals.cell_size,
            speed = 0,
            type=bonus_type,
            x=bonus_x, y=bonus_y,
            color=(255, 255, 255),
            layer=251,
            entity_group=globals.entities
        )
        break

def game(**kwargs):
    is_setup = kwargs.get("is_setup", False)
    if is_setup:
        setup_game(**kwargs)
        return

    go_menu_button_sprite = paint_api.mount_rect(px_x=0, px_y=0, px_w=40, px_h=40, layer=300, key="go_menu")

    if is_clicked(go_menu_button_sprite):
        navigate("menu")

    # if player1_sprite.collides_with(player2_sprite):
    #     print("Che tam")
    # print(SurfaceSprite.SurfaceId)
    globals.tick += 1
    if globals.tick % 150 == 0:
        spawn_bonus(bonus_types()[rand(0, 3)])
    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        entity.add_tick()

        if isinstance(entity, Controllable):
            entity.handle_event()
        if isinstance(entity, BotIntellect):
            entity.think()
        if isinstance(entity, Collidable):
            entity.handle_collision()
