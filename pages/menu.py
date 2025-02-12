import pygame.sprite

import globals
import paint_api
from pygame.locals import *

from pages.navigation import navigate


def menu():
    paint_api.draw_rect(px_x=300, px_y=30, px_w=200, px_h=80, key="play")
    paint_api.draw_rect(px_x=300, px_y=120, px_w=200, px_h=80, key="settings")

    click_pos = None

    for event in globals.frame_events:
        if event.type == MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()

    if click_pos:
        for sprite in reversed(globals.all_sprites.sprites()):
            if sprite.rect.collidepoint(click_pos):
                navigate("game")
                break
