import pygame
from pygame.locals import *

import globals
from utils.event_api import is_fired
from utils.paint_api import is_mounted


def is_clicked(sprite):
    if not is_mounted(sprite):
        return False
    if is_fired(MOUSEBUTTONDOWN, 1):
        click_pos = pygame.mouse.get_pos()
    else:
        return False

    return sprite.rect.collidepoint(click_pos)


def is_pressed(event_key):
    return globals.frame_keys[event_key]
