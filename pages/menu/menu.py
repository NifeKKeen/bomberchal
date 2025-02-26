import sys
import pygame
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked


def menu(is_setup):
    if is_setup:
        pygame.mixer.music.load("assets/sound/menu3.mp3")
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1)

    play_button_sprite = paint_api.mount_rect(
        px_x=300,
        px_y=30,
        px_w=200,
        px_h=80,
        key="play",
        title="Play",
    )
    settings_button_sprite = paint_api.mount_rect(
        px_x=300, px_y=120, px_w=200, px_h=80, key="settings"
    )
    test_button_sprite = paint_api.mount_rect(
        px_x=300, px_y=210, px_w=200, px_h=80
    )  # if key is not specified, it will render over and over
    quit_button_sprite = paint_api.mount_rect(
        px_x=300, px_y=300, px_w=200, px_h=80, key="quit", title="Quit"
    )

    if is_clicked(play_button_sprite):
        navigate("game")
    elif is_clicked(settings_button_sprite):
        navigate("menu/settings")
    elif is_clicked(quit_button_sprite):
        pygame.quit()
        sys.exit()