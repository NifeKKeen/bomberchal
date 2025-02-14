from pages.game import field_generator
from pages.game.game import *
from utils import paint_api
from pygame.locals import *

from pages.navigation import navigate
from entitites.player import get_players, Player
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
        player = Player(
            px_x=(1 if i == 0 else 19) * globals.cell_size, px_y=(1 if i == 0 else 19) * globals.cell_size,
            px_w=globals.cell_size, px_h=globals.cell_size,
            speed=rand(1, 10),
            color=(0, rand(128, 256), rand(128, 256)),
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
                                    px_w = globals.cell_size, px_h = globals.cell_size, key = str(x) + ";" + str(y),
                                                       color=(64, 64, 64))
                obstacle_sprite.mount()
                Obstacles.append((obstacle_sprite, globals.U_OBSTACLE_CELL))
            elif field[x][y] == globals.D_OBSTACLE_CELL:
                obstacle_sprite = paint_api.mount_rect(px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                                    px_w = globals.cell_size, px_h = globals.cell_size, key = str(x) + ";" + str(y),
                                                       color=((255, 255, 64)))
                                                       #color=(((x + y) % 2) * 255, 255, 0)) #chess-like
                obstacle_sprite.mount()
                Obstacles.append((obstacle_sprite, globals.D_OBSTACLE_CELL))

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
    if is_clicked(player1_sprite):
        player1_sprite.unmount()
    if is_clicked(player2_sprite):
        player2_sprite.unmount()

    if player1_sprite.alive():

        if is_pressed(K_w):
            player1_sprite.move_px(0, -player1_sprite.speed)
            if player1_sprite.collides_with(player2_sprite):
                player1_sprite.move_px(0, player2_sprite.y - player1_sprite.y)
        if is_pressed(K_s):
            player1_sprite.move_px(0, +player1_sprite.speed)
            if player1_sprite.collides_with(player2_sprite):
                player1_sprite.move_px(0, -player1_sprite.speed)
        if is_pressed(K_a):
            player1_sprite.move_px(-player1_sprite.speed, 0)
            if player1_sprite.collides_with(player2_sprite):
                player1_sprite.move_px(+player1_sprite.speed, 0)
        if is_pressed(K_d):
            player1_sprite.move_px(+player1_sprite.speed, 0)
            if player1_sprite.collides_with(player2_sprite):
                player1_sprite.move_px(-player1_sprite.speed, 0)

    if player2_sprite.alive():
        if is_pressed(K_UP):
            player2_sprite.move_px(0, -player2_sprite.speed)
        if is_pressed(K_DOWN):
            player2_sprite.move_px(0, +player2_sprite.speed)
        if is_pressed(K_LEFT):
            player2_sprite.move_px(-player2_sprite.speed, 0)
        if is_pressed(K_RIGHT):
            player2_sprite.move_px(+player2_sprite.speed, 0)
        if is_pressed_once(K_RETURN):
            player2_sprite.spawn_bomb()

    # if player1_sprite.collides_with(player2_sprite):
    #     print("Che tam")

    globals.tick += 1
    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        entity.add_tick()