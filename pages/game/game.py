from entitites.bomb import Bomb
from entitites.bot import Bot
from globals import directions
from pages.game import field_generator
from pages.game.game import *
from utils import paint_api
from pygame.locals import *

from pages.navigation import navigate
from entitites.player import get_players, Player, get_bombs
from utils.helpers import rand
from utils.interaction_api import is_clicked, is_pressed, is_pressed_once
import globals

DEFAULT_FIELD = [
    [globals.VOID_CELL if rand(0, 100) < 50 else globals.U_OBSTACLE_CELL for j in range(20)] for i in range(20)
]
Obstacles = []

def setup_game(**kwargs):
    globals.cols = kwargs.get("cols", 21)
    globals.rows = kwargs.get("rows", 21)
    globals.field = kwargs.get("field", field_generator.generate(globals.rows, globals.cols))
    for i in range(2):
        rnd = rand(192, 256)
        player = Player(
            px_x=(1 if i == 0 else 19) * globals.cell_size, px_y=(1 if i == 0 else 19) * globals.cell_size,
            px_w=globals.cell_size, px_h=globals.cell_size,
            speed=2,
            color=(0, rnd / 2, rnd),
            layer=260,
            bomb_allowed=5,
            entity_group=globals.entities,
            key=f"player-{i}"
        )
        player.mount()

    render_field()

def render_field(**kwargs):
    field = globals.field
    for i in field:
        print(i)
    cols = globals.cols
    rows = globals.rows
    global Obstacles
    for x in range(cols):
        for y in range(rows):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                obstacle_sprite = paint_api.mount_rect(px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                                    px_w = globals.cell_size, px_h = globals.cell_size,
                                                       key = str(x) + ";" + str(y),
                                                       color=(64, 64, 64))
                obstacle_sprite.mount()
                Obstacles.append((obstacle_sprite, globals.U_OBSTACLE_CELL))
            elif field[x][y] == globals.D_OBSTACLE_CELL:
                obstacle_sprite = paint_api.mount_rect(px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                                    px_w = globals.cell_size, px_h = globals.cell_size,
                                                       key = str(x) + ";" + str(y),
                                                       color=(255, 255, 64))
                obstacle_sprite.mount()
                Obstacles.append((obstacle_sprite, globals.D_OBSTACLE_CELL))
            elif field[x][y] == globals.BOT_CELL:
                bot = Bot(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    speed=2,
                    color=(13*x, 13*y, 92 * ((x + y) % 2)),
                    layer=250,
                    entity_group=globals.entities,
                    key=f"bot-{x},{y}"
                )
                bot.mount()
                globals.entities.add(bot)

def explosion_spread(**kwargs):  # actually it just spawns new bombs in adjacent cells
    bombs = get_bombs(globals.entities)
    new_bombs = set()

    for bomb in bombs:
        if bomb.power > 5:
            continue
        globals.entities.remove(bomb)

        for dx, dy in globals.directions:
            new_bomb = Bomb(
                spawner=bomb.spawner,
                px_w=bomb.px_w,
                px_h=bomb.px_h,
                px_x=bomb.px_x + dx * globals.cell_size,
                px_y=bomb.px_y + dy * globals.cell_size,
                layer=bomb.layer,
                timer=bomb.timer,
                color=bomb.color,
                power=bomb.power + 1,
                entity_group=globals.entities,
            )
            new_bomb.mount()
            new_bombs.add(new_bomb)

    globals.entities.update(new_bombs)



def reset_game():
    globals.entities.clear()


def game(**kwargs):
    is_setup = kwargs.get("is_setup", False)
    if is_setup:
        setup_game(**kwargs)
        return

    go_menu_button_sprite = paint_api.mount_rect(px_x=0, px_y=0, px_w=40, px_h=40, layer=300, key="go_menu")

    player1_sprite = list(get_players(globals.entities))[0]
    player2_sprite = list(get_players(globals.entities))[1]

    if is_clicked(go_menu_button_sprite):
        navigate("menu")


    players_params = [
        [player1_sprite, K_w, K_s, K_a, K_d, K_SPACE],
        [player2_sprite, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN],
    ]

    for player in players_params:
        if is_clicked(player[0]):
            player[0].unmount()

        if player[0].alive():
            if is_pressed(player[1]):
                player[0].move_px(0, -player[0].speed)
                # if player[0].collides_with(player2_sprite):
                #     player[0].move_px(0, +player[0].speed)
                # for obstacle in Obstacles:
                #     if player[0].collides_with(obstacle[0]):
                #         player[0].move_px(0, obstacle[0].px_y - player[0].y)
                #         break

            if is_pressed(player[2]):
                player[0].move_px(0, +player[0].speed)
            if is_pressed(player[3]):
                player[0].move_px(-player[0].speed, 0)
            if is_pressed(player[4]):
                player[0].move_px(+player[0].speed, 0)

            if is_pressed(player[5]):
                player[0].spawn_bomb()

    explosion_spread()

    # if player1_sprite.collides_with(player2_sprite):
    #     print("Che tam")

    globals.tick += 1
    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        entity.add_tick()