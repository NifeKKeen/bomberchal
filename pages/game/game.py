import globals
from pygame.locals import *

from entitites.bot import Bot
from utils import paint_api
from utils.helpers import rand, get_field_pos, get_tick_from_ms
from utils.interaction_api import is_clicked
from utils.paint_api import mount_rect
from utils.sound_api import play_music
from entitites.bonus import Bonus, bonus_types
from entitites.interfaces.BotIntellect import BotIntellect
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.obstacle import Obstacle
from entitites.player import Player
from pages.game import field_generator
from pages.navigation import navigate

DEFAULT_FIELD = [
    [globals.VOID_CELL if rand(0, 100) < 50 else globals.U_OBSTACLE_CELL for j in range(20)] for i in range(20)
]

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
    globals.field = kwargs.get("field", field_generator.generate(globals.cols, globals.rows))
    globals.field_fire_state = kwargs.get("field_fired",
        [[0] * globals.rows for _ in range(globals.cols)]
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
            speed=2,
            lives=3,
            bomb_power=7,
            bomb_allowed=5,
            bomb_timer=get_tick_from_ms(3000),
            character_skin_key=f"ch{rand(1, 5)}",

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
    for i in field:
        print(i)
    rows = globals.rows
    cols = globals.cols
    for x in range(cols):
        for y in range(rows):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                obstacle_sprite = Obstacle(
                    type=field[x][y],
                    seed=0,

                    color=(64, 64, 64),
                    entity_group=globals.entities,

                    key = f"o-{x};{y}",
                    x=x,
                    y=y,
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w = globals.cell_size, px_h = globals.cell_size,
                )


            elif field[x][y] == globals.D_OBSTACLE_CELL:
                obstacle_seed = rand(1, 3)

                obstacle_sprite = Obstacle(
                    type=field[x][y],
                    seed=obstacle_seed,

                    color=(255, 255, 64),
                    entity_group=globals.entities,

                    key = f"o-{x};{y}",
                    x=x,
                    y=y,
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w = globals.cell_size, px_h = globals.cell_size,
                )


            elif field[x][y] == globals.BOT_CELL:
                bot_type = rand(1, 4)
                bot = Bot(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    #px_w=globals.player_cell_size, px_h=globals.player_cell_size,
                    x=x, y=y,
                    speed=1,
                    color=[(0, 255, 0), (0, 0, 255), (255, 0, 0)][bot_type - 1],
                    layer=256,
                    entity_group=globals.entities,
                    type=bot_type
                )

    for i in range(1, 10):
        for player in range(2):
            print((i - 1) * globals.cell_size, (globals.rows + player) * globals.cell_size)
            paint_api.mount_text(
                text=str(i),
                font_size=30,
                color=(255, 255, 255),

                key=f"bonus-{i}-{player}",
                px_x=(i - 1) * globals.cell_size,
                px_y=(globals.rows + player) * globals.cell_size,
            )

def reset_game():
    globals.entities.clear()

def spawn_bonus(bonus_type = 0):
    while True:
        bonus_x, bonus_y = rand(0, globals.cols), rand(0, globals.rows)
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
            type=bonus_types()[bonus_type],

            color=[(123, 123, 0), (123, 0, 123), (0, 123, 123)][bonus_type],

            layer=251,
            entity_group=globals.entities,

            x=bonus_x,
            y=bonus_y,
            px_x=bonus_x * globals.cell_size, px_y=bonus_y * globals.cell_size,
            px_w=globals.cell_size, px_h=globals.cell_size,
        )
        break

def render_bonuses():
    for entity in list(globals.entities):
        if not isinstance(entity, Player):# and not isinstance(entity, Bot):
            continue
        # Player or bot
        for bonus in entity.bonuses:
            if entity.key[-1] == '0':
                if bonus.y != globals.rows:
                    bonus.x = len(entity.bonuses) - 1
                    bonus.y = globals.rows
            else:
                if bonus.y != globals.rows + 1:
                    bonus.x = len(entity.bonuses) - 1
                    bonus.y = globals.rows + 1

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

    # if player1_sprite.collides_with(player2_sprite):
    #     print("Che tam")
    # print(SurfaceSprite.SurfaceId)
    # if globals.tick % 20 == 0:
    #     spawn_bonus(rand(0, 3))

    # if len(get_players(globals.entities)) == 0:
    #     raise Exception("You lost")

    # render_bonuses()

    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        if isinstance(entity, Controllable):
            entity.handle_event()
        if isinstance(entity, BotIntellect):
            entity.think()
        if isinstance(entity, Collidable):
            entity.handle_collision()
        if isinstance(entity, Bonus) and entity.timer > 0:
            entity.timer -= 1
