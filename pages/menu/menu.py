import sys
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked

import globals
from utils.sound_api import play_menu_music, stop_music


def menu(is_setup = False):
    if is_setup:
        play_menu_music(volume=.2)

    mute_button_sprite = paint_api.mount_rect(
        px_x=globals.center_x - 380,
        px_y=globals.center_y - 200,    
        px_w=65,
        px_h=65,
        key="mute",
        image_path="assets/images/buttons/bar_button.png",
    )
    play_button_sprite = paint_api.mount_rect(
        px_y=globals.center_y - 100,
        px_w=460,
        px_h=90,
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
        px_w=460,
        px_h=90, 
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
        px_w=460,
        px_h=90, 
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
        sys.exit()
    elif is_clicked(mute_button_sprite):
        if globals.music_muted:
            globals.music_muted = False
            play_menu_music(volume=.2)
        else:
            globals.music_muted = True
            stop_music()
