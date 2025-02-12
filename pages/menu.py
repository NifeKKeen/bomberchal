import pygame.sprite

import globals
from utils import paint_api
from pygame.locals import *

from utils.event_api import is_fired
from pages.navigation import navigate
from utils.interaction_api import is_clicked


def menu():
    play_button_sprite = paint_api.mount_rect(px_x=300, px_y=30, px_w=200, px_h=80, key="play")
    settings_button_sprite = paint_api.mount_rect(px_x=300, px_y=120, px_w=200, px_h=80, key="settings")

    if is_clicked(play_button_sprite):
        navigate("game")

    elif is_clicked(settings_button_sprite):
        navigate("settings")
