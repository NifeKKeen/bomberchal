import pygame.sprite

import globals
from entitites.player import Player
from utils import paint_api
from pygame.locals import *

from utils.event_api import is_fired
from pages.navigation import navigate
from utils.interaction_api import is_clicked, is_pressed


def game(**kwargs):
    cols = kwargs.get("cols", 1)
    rows = kwargs.get("cols", 1)

    go_menu_button_sprite = paint_api.mount_rect(px_x=0, px_y=0, px_w=40, px_h=40, key="go_menu")
    player_sprite = paint_api.mount_sprite(Player(px_x=0, px_y=0, px_w=30, px_h=30, key="player1"))

    # TODO
    if is_clicked(go_menu_button_sprite):
        navigate("menu")
    elif is_pressed(K_w):
        player_sprite.rect.y -= 1
    elif is_pressed(K_s):
        player_sprite.rect.y += 1
    elif is_pressed(K_a):
        player_sprite.rect.x -= 1
    elif is_pressed(K_d):
        player_sprite.rect.x += 1
