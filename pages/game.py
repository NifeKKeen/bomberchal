import pygame.sprite

import globals
import paint_api
from pygame.locals import *

from pages.navigation import navigate


def game():
    paint_api.draw_rect(px_x=600, px_y=30, px_w=200, px_h=80, key="test")
    paint_api.draw_rect(px_x=600, px_y=120, px_w=200, px_h=80, key="cell1")

    click_pos = None

    for event in globals.frame_events:
        if event.type == MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()

    if click_pos:
        for sprite in reversed(globals.all_sprites.sprites()):
            if sprite.rect.collidepoint(click_pos):
                navigate("menu")
                break
