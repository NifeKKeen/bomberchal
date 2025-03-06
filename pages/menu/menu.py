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
        px_y=globals.center_y - 100,
        px_w=350,
        px_h=85,
        key="play",
        image_path="assets/images/buttons/bar_button.png",
        align="center"
    )
    play_center = play_button_sprite.rect.center

    play_button_shadow = paint_api.mount_text(
        px_x = play_center[0] + 4,
        px_y = play_center[1] + 4,
        key = "play_text_shadow",
        text="Play",
        font_size=50,
        color=(0, 0, 0)
    )
    play_button_text = paint_api.mount_text(
        px_x = play_center[0],
        px_y = play_center[1],
        key = "play_text",
        text="Play",
        font_size=50,
        color=(255, 255, 255)
    )

    settings_button_sprite = paint_api.mount_rect(
        px_y=globals.center_y,
        px_w=350,
        px_h=85, 
        key="settings", 
        image_path="assets/images/buttons/bar_button.png",
        align="center"
    )
    settings_center = settings_button_sprite.rect.center
    settings_button_shadow = paint_api.mount_text(
        px_x = play_center[0] + 4,
        px_y = play_center[1] + 4,
        key = "settings_text_shadow",
        text="Settings",
        font_size=50,
        color=(0, 0, 0)
    )
    settings_button_text = paint_api.mount_text(
        px_x = settings_center[0],
        px_y = settings_center[1],
        key="settings_text",
        text="Settings",
        font_size=50,
        color=(255, 255, 255)
    )

    quit_button_sprite = paint_api.mount_rect(
        px_y=globals.center_y + 100,
        px_w=350,
        px_h=85, 
        key="quit", 
        image_path="assets/images/buttons/bar_button.png",
        align="center"
    )
    quit_center = quit_button_sprite.rect.center
    quit_button_shadow = paint_api.mount_text(
        px_x = quit_center[0] + 4,
        px_y = quit_center[1] + 4,
        key = "quit_text_shadow",
        text="Quit",
        font_size=50,
        color=(0, 0, 0)
    )
    quit_button_text = paint_api.mount_text(
        px_x = quit_center[0],
        px_y = quit_center[1],
        key="quit_text",
        text="Quit",
        font_size=50,
        color=(255,255,255)
    )

    for button_text, button_shadow, center in [
        (play_button_text, play_button_shadow, play_center),
        (settings_button_text, settings_button_shadow, settings_center),
        (quit_button_text, quit_button_shadow, quit_center)
    ]:
        button_text.rect.center = center
        button_shadow.rect.center = (center[0] + 4, center[1] + 4)

    if is_clicked(play_button_sprite):
        navigate("game")
    elif is_clicked(settings_button_sprite):
        navigate("menu/settings")
    elif is_clicked(quit_button_sprite):
        pygame.quit()
        sys.exit()