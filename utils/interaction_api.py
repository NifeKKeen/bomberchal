import pygame
from pygame.locals import *

import globals
from utils.event_api import is_fired

map_event_type_to_pressed_event_type = {
    119: 1024
}


def is_clicked(sprite):
    if is_fired(MOUSEBUTTONDOWN):
        click_pos = pygame.mouse.get_pos()
    else:
        return False

    return sprite.rect.collidepoint(click_pos)


def is_pressed(pressed_event_type):
    print(globals.frame_events, pressed_event_type)
    return is_fired(map_event_type_to_pressed_event_type.get(pressed_event_type, -1))
