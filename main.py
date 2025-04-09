import pygame
import sys
from pygame.locals import *

from pages.menu.menu import menu
from pages.menu.play import play
from pages.menu.settings import settings
from pages.menu.customization import customization
from pages.menu.scoreboard import scoreboard
from utils import paint_api
from pages.game.game import game
import globals
from utils.db_api import get_db_connection
from utils.interaction_api import get_pressed_keys
from utils.paint_api import draw_sprites, GIFSprite

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Bomberchal")

    globals.DISPLAYSURF = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
    globals.Frame = pygame.time.Clock()

    globals.all_sprites = pygame.sprite.LayeredUpdates()
    globals.brown_background_img = pygame.image.load("assets/images/backgrounds/settings.jpg")
    globals.brown_background_img = pygame.transform.scale(
        globals.brown_background_img,
        (globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT)
    )
    globals.menu_background_img = pygame.image.load("assets/images/backgrounds/menu.jpg")
    globals.menu_background_img = pygame.transform.scale(
        globals.menu_background_img,
        (globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT)
    )

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
            if event.type == KEYDOWN:
                globals.comba.append(event.unicode)
                if len(globals.comba) > 10:
                    globals.comba.pop(0)
                if "".join(globals.comba) == "js>python":
                    globals.KRASAVA = True
                globals.frame_unicodes.add(event.unicode)

        globals.frame_keys_map = pygame.key.get_pressed()
        globals.frame_keys = get_pressed_keys()
        globals.frame_event_types.add(event.type)

        globals.tick += 1

        # Page navigation

        if globals.current_page == "menu":
            menu(is_setup=globals.switched_page_this_frame)
        elif globals.current_page == "menu/play":
            play(is_setup=globals.switched_page_this_frame)
        elif globals.current_page == "menu/settings":
            settings(is_setup=globals.switched_page_this_frame)
        elif globals.current_page == "menu/customization":
            customization()
        elif globals.current_page == "menu/scoreboard":
            scoreboard(is_setup=globals.switched_page_this_frame)
        elif globals.current_page == "game":
            game(is_setup=globals.switched_page_this_frame)

        draw_sprites()

        for sprite in list(globals.all_sprites):  # list to avoid "Set changed size during iteration" error
            if isinstance(sprite, GIFSprite):
                sprite.process_gif()

        # Clean up
        globals.frame_event_code_pairs.clear()
        globals.frame_unicodes.clear()
        globals.frame_event_types.clear()
        globals.frame_keys.clear()

        # Check if the page was NOT switched during this frame
        if not globals.switched_page:
            # Since no switch occurred, reset the flag for next frame
            globals.switched_page_this_frame = False
