from copy import deepcopy

import globals
from entitites.player import Player
from utils import paint_api
from pygame.locals import *

from pages.navigation import navigate
from entitites.player import get_players
from utils.helpers import rand
from utils.interaction_api import is_clicked, is_pressed

DEFAULT_FIELD = [
    [globals.VOID_CELL if rand(0, 100) < 50 else globals.U_OBSTACLE_CELL for j in range(20)] for i in range(20)
]


def setup_game(**kwargs):
    globals.cols = kwargs.get("cols", 20)
    globals.rows = kwargs.get("rows", 20)
    globals.field = kwargs.get("field", deepcopy(DEFAULT_FIELD))
    for i in range(2):
        player = Player(
            px_x=0, px_y=0,
            px_w=50, px_h=50,
            speed=rand(1, 10),
            color=(0, rand(128, 256), rand(126, 256)),
            key=f"player-{i}"
        )
        player.enable()
        globals.entities.append(player)


def reset_game():
    globals.entities.clear()


def game(**kwargs):
    is_setup = kwargs.get("is_setup", False)
    if is_setup:
        setup_game(**kwargs)
        return

    go_menu_button_sprite = paint_api.mount_rect(px_x=0, px_y=0, px_w=40, px_h=40, key="go_menu")

    player1_sprite = get_players(globals.entities)[0]
    player2_sprite = get_players(globals.entities)[1]

    if is_clicked(go_menu_button_sprite):
        navigate("menu")
    if is_clicked(player1_sprite):
        player1_sprite.disable()
    if is_clicked(player2_sprite):
        player2_sprite.disable()

    if player1_sprite.alive():
        if is_pressed(K_w):
            player1_sprite.rect.y -= player1_sprite.speed
        if is_pressed(K_s):
            player1_sprite.rect.y += player1_sprite.speed
        if is_pressed(K_a):
            player1_sprite.rect.x -= player1_sprite.speed
        if is_pressed(K_d):
            player1_sprite.rect.x += player1_sprite.speed
    if player2_sprite.alive():
        if is_pressed(K_UP):
            player2_sprite.rect.y -= player2_sprite.speed
        if is_pressed(K_DOWN):
            player2_sprite.rect.y += player2_sprite.speed
        if is_pressed(K_LEFT):
            player2_sprite.rect.x -= player2_sprite.speed
        if is_pressed(K_RIGHT):
            player2_sprite.rect.x += player2_sprite.speed
