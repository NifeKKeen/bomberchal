import pygame, sys
from pygame.locals import *

from pages.game import reset_game
from utils import paint_api
from pages import menu, game
import globals
from utils.paint_api import draw_sprites

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Bomberchal")

    globals.DISPLAYSURF = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
    globals.Frame = pygame.time.Clock()

    globals.all_sprites = pygame.sprite.LayeredUpdates()

    while True:
        if globals.switched_page:
            paint_api.reset()
            globals.switched_page = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                globals.frame_events.add((event.type, event.button))

            globals.frame_keys = pygame.key.get_pressed()


        # Page navigation

        if globals.current_page == "menu":
            menu.menu()
        # elif globals.current_page == "menu/settings":
        #     menu_settings()
        # elif globals.current_page == "menu/customization":
        #     menu_customization()
        # elif globals.current_page == "menu/scoreboard":
        #     menu_scoreboard()
        elif globals.current_page == "game":
            game.game(is_setup=globals.switched_page_this_frame)

        if not globals.current_page.startswith("game"):
            reset_game()

        draw_sprites()

        globals.Frame.tick(globals.FPS)
        globals.frame_events.clear()

        # Check if the page was NOT switched during this frame
        if not globals.switched_page:
            # Since no switch occurred, reset the flag for next frame
            globals.switched_page_this_frame = False
