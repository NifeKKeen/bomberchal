import globals, pygame
from pygame.locals import *
from utils.event_api import is_fired


is_waiting_for_key = False  # глобальное состояние ожидания нажатия клавиши

def is_clicked(sprite):
    if not sprite.mounted:
        return False
    if is_fired(MOUSEBUTTONDOWN, 1):
        click_pos = pygame.mouse.get_pos()
    else:
        return False

    return sprite.rect.collidepoint(click_pos)


def is_pressed(event_key):
    return globals.frame_keys_map[event_key]

def is_pressed_once(event_key):
    return is_fired(KEYDOWN, event_key)


def get_pressed_keys():  # is already called in main.py, use globals.frame_keys instead
    keys = []
    for event_type, key in globals.frame_event_code_pairs:
        if event_type == KEYDOWN:
            keys.append(key)
    return keys

def get_last_pressed_key():
    return globals.frame_keys[-1] if globals.frame_keys else None
