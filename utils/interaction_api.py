import pygame
from pygame.locals import *

import globals
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
    return globals.frame_keys[event_key]

def is_pressed_once(event_key):
    return is_fired(KEYDOWN, event_key)

def get_pressed_key():
    global is_waiting_for_key
    is_waiting_for_key = True  # устанавливаем режим ожидания
    # вместо блокировки ждем один проход событий
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            is_waiting_for_key = False
            return event.key
    is_waiting_for_key = False
    return None

