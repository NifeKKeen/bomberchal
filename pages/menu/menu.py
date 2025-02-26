import sys
import pygame
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked

import globals

def menu(is_setup):
    if is_setup:
        pygame.mixer.music.load("assets/sound/menu3.mp3")
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1)

    play_button_sprite = paint_api.mount_rect(
        px_y=globals.center_y - 90,
        px_w=200,
        px_h=80,
        key="play",
        image_path="assets/images/buttons/play.png",
        align="center"
    )
    settings_button_sprite = paint_api.mount_rect(
        px_y=globals.center_y,
        px_w=350,
        px_h=90, 
        key="settings", 
        image_path="assets/images/buttons/settings.png",
        align="center"
    )
    quit_button_sprite = paint_api.mount_rect(
        px_y=globals.center_y + 90,
        px_w=200,
        px_h=80, 
        key="quit", 
        image_path="assets/images/buttons/quit.png",
        align="center"
    )
    # test_button_sprite = paint_api.mount_rect(
    #     px_x=300, px_y= 410, px_w=200, px_h=80
    # )  # if key is not specified, it will render over and over

    if is_clicked(play_button_sprite):
        navigate("game")
    elif is_clicked(settings_button_sprite):
        navigate("menu/settings")
    elif is_clicked(quit_button_sprite):
        pygame.quit()
        sys.exit()