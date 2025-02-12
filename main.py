import pygame, sys
from pygame.locals import *

import paint_api
from globals import frame_events, all_sprites, to_render_keys
from pages import menu, game
import globals
from paint_api import draw_sprites

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
            globals.frame_events.append(event)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

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
            game.game()

        draw_sprites()

        globals.Frame.tick(globals.FPS)
        globals.frame_events.clear()
