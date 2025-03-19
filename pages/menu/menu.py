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
        image_path=globals.muted_img if globals.music_muted else globals.unmuted_img,
    )
    play_button_sprite = paint_api.mount_rect(
        px_y=globals.center_y - 100,
        px_w=500,
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
        color=(0, 0, 0),
        align = "center"
    )
    play_button_text = paint_api.mount_text(
        px_x = play_center[0] ,
        px_y = play_center[1] ,
        key = "play_text",
        text="Play",
        font_size=50,
        color=(255, 255, 255),
        align = "center"
    )
    customization_button_sprite = paint_api.mount_rect(
        px_y=globals.center_y,
        px_w=500,
        px_h=90, 
        key="customization",
        image_path="assets/images/buttons/bar_button.png",
        align="center"
    )
    customization_center = customization_button_sprite.rect.center
    customization_button_shadow = paint_api.mount_text(
        px_x = customization_center[0] + 4,
        px_y = customization_center[1] + 4,
        key = "customization_text_shadow",
        text="Customization",
        font_size=50,
        color=(0, 0, 0),
        align = "center"
    )
    customization_button_text = paint_api.mount_text(
        px_x = customization_center[0],
        px_y = customization_center[1],
        key="customization_text",
        text="Customization",
        font_size=50,
        color=(255, 255, 255),
        align = "center"
    )
    settings_button_sprite = paint_api.mount_rect(
        px_x=globals.center_x - 250,
        px_y=globals.center_y + 55,
        px_w=240,
        px_h=90,
        key="settings",
        image_path="assets/images/buttons/bar_button.png",
        # align="center"
    )
    settings_center = settings_button_sprite.rect.center
    settings_button_shadow = paint_api.mount_text(
        px_x = settings_center[0] + 4,
        px_y = settings_center[1] + 4,
        key = "settings_text_shadow",
        text="Settings",
        font_size=50,
        color=(0, 0, 0),
        align = "center"
    )
    settings_button_text = paint_api.mount_text(
        px_x = settings_center[0],
        px_y = settings_center[1],
        key="settings_text",
        text="Settings",
        font_size=50,
        color=(255, 255, 255),
        align = "center"
    )
    # scoreboard_button_sprite = paint_api.mount_rect(
    #     px_y=globals.center_y + 200,
    #     px_w=230,
    #     px_h=90,
    #     key="scoreboard",
    #     image_path="assets/images/buttons/bar_button.png",
    #     align="center"
    # )
    # scoreboard_center = scoreboard_button_sprite.rect.center
    # scoreboard_button_shadow = paint_api.mount_text(
    #     px_x = scoreboard_center[0] + 4,
    #     px_y = scoreboard_center[1] + 4,
    #     key = "scoreboard_text_shadow",
    #     text="Scoreboard",
    #     font_size=50,
    #     color=(0, 0, 0)
    # )
    # scoreboard_button_text = paint_api.mount_text(
    #     px_x = scoreboard_center[0],
    #     px_y = scoreboard_center[1],
    #     key="scoreboard_text",
    #     text="Scoreboard",
    #     font_size=50,
    #     color=(255, 255, 255)
    # )



    quit_button_sprite = paint_api.mount_rect(
        px_x=globals.center_x,
        px_y=globals.center_y + 55,
        px_w=250,
        px_h=90, 
        key="quit", 
        image_path="assets/images/buttons/bar_button.png",
    )
    quit_center = quit_button_sprite.rect.center
    quit_button_shadow = paint_api.mount_text(
        px_x = quit_center[0] + 4,
        px_y = quit_center[1] + 4,
        key = "quit_text_shadow",
        text="Quit",
        font_size=50,
        color=(0, 0, 0),
        align = "center"
    )
    quit_button_text = paint_api.mount_text(
        px_x = quit_center[0],
        px_y = quit_center[1],
        key="quit_text",
        text="Quit",
        font_size=50,
        color=(255,255,255),
        align = "center"
    )

    if is_clicked(play_button_sprite):
        navigate("game")
    elif is_clicked(settings_button_sprite):
        navigate("menu/settings")
    # elif is_clicked(scoreboard_button_sprite):
    #     navigate("menu/scoreboard")
    elif is_clicked(customization_button_sprite):
        navigate("menu/customization")
    elif is_clicked(quit_button_sprite):
        sys.exit()

    elif is_clicked(mute_button_sprite):
        if globals.music_muted:
            globals.music_muted = False
            play_menu_music(volume=.2)
            mute_button_sprite.set_image_path(globals.unmuted_img)
        else:
            globals.music_muted = True
            stop_music()
            mute_button_sprite.set_image_path(globals.muted_img)
