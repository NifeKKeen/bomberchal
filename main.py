import pygame, sys
from pygame.locals import *

from entitites.entity import Entity
from entitites.interfaces.BombSpawnable import BombSpawnable
from pages.menu.menu import menu
from pages.menu.settings import settings
from pages.menu.customization import menu_customization
from pages.menu.scoreboard import menu_scoreboard 
from utils import paint_api
from pages.game.game import reset_game, game
import globals
from utils.interaction_api import get_pressed_keys
from utils.paint_api import draw_sprites, GIFSprite

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Bomberchal")

    globals.DISPLAYSURF = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
    globals.Frame = pygame.time.Clock()

    globals.all_sprites = pygame.sprite.LayeredUpdates()
    globals.brown_background_img = pygame.image.load("assets/images/backgrounds/settings.jpg")
    globals.brown_background_img = pygame.transform.scale(globals.brown_background_img, (globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
    globals.menu_background_img = pygame.image.load("assets/images/backgrounds/menu.jpg")
    globals.menu_background_img = pygame.transform.scale(globals.menu_background_img, (globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))


    while True:
        if globals.switched_page:
            paint_api.reset_frame()
            globals.switched_page = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                globals.frame_event_code_pairs.add((event.type, event.button))
            if event.type in (KEYDOWN, KEYUP):
                globals.frame_event_code_pairs.add((event.type, event.key))
            globals.frame_event_types.add(event.type)

            globals.frame_keys_map = pygame.key.get_pressed()
            globals.frame_keys = get_pressed_keys()


        # Page navigation

        if globals.switched_page_this_frame and not globals.current_page.startswith("game"):
            reset_game()

        if globals.current_page == "menu":
            menu(is_setup=globals.switched_page_this_frame)
        elif globals.current_page == "menu/settings":
            settings(is_setup=globals.switched_page_this_frame)
        elif globals.current_page == "menu/customization":
            menu_customization()
        elif globals.current_page == "menu/scoreboard":
            menu_scoreboard()
        elif globals.current_page == "game":
            game(is_setup=globals.switched_page_this_frame)

        draw_sprites()

        globals.tick += 1
        for sprite in list(globals.all_sprites):  # list to avoid "Set changed size during iteration" error
            if isinstance(sprite, Entity):
                sprite.add_tick()
                sprite.cur_damage_countdown = max(sprite.cur_damage_countdown - 1, 0)
            if isinstance(sprite, BombSpawnable):
                sprite.add_tick()
                sprite.cur_bomb_countdown = max(sprite.cur_bomb_countdown - 1, 0)
            if isinstance(sprite, GIFSprite):
                sprite.process_gif()
        globals.Frame.tick(globals.FPS)

        # Clean up
        globals.frame_event_code_pairs.clear()
        globals.frame_event_types.clear()
        globals.frame_keys.clear()

        # Check if the page was NOT switched during this frame
        if not globals.switched_page:
            # Since no switch occurred, reset the flag for next frame
            globals.switched_page_this_frame = False
