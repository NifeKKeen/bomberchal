import globals, pygame
from pygame.locals import *
from utils.event_api import is_fired


def is_clicked(sprite, should_check_layers = False):
    if sprite is None or not sprite.mounted:
        return False
    if is_fired(MOUSEBUTTONDOWN, 1):
        click_pos = pygame.mouse.get_pos()
    else:
        return False

    if not sprite.rect.collidepoint(click_pos):
        return False
    if not should_check_layers:
        return True

    sprites_touched = globals.all_sprites.get_sprites_at(click_pos)
    topmost_sprite = max(  # sprite with the highest layer
        sprites_touched,
        key=lambda cur_sprite: cur_sprite._layer
    )
    return topmost_sprite == sprite


def are_clicked(*sprites):
    for sprite in sprites:
        if is_clicked(sprite, True):
            return True
    return False


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


def get_pressed_chars():  # is already called in main.py, use globals.frame_keys instead
    chars = []
    for event_type, key in globals.frame_event_code_pairs:
        if event_type == KEYDOWN:
            chars.append(key)
    return chars


def get_last_pressed_key():
    return globals.frame_keys[-1] if globals.frame_keys else None


def get_last_pressed_char():
    for ch in globals.frame_unicodes:
        if ch:
            return ch

    return ""
