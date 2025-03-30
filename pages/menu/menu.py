import globals
import sys

from pygame import K_BACKSPACE, K_RETURN
from config import save_config, load_config
from pages.navigation import navigate
from utils import paint_api
from utils.interaction_api import is_clicked, get_last_pressed_key, get_last_pressed_char, are_clicked, is_pressed_once
from utils.paint_api import mount_button
from utils.sound_api import play_menu_music, stop_music

INPUT_PLACEHOLDER_TEXT = "Enter your name..."

mute_button_sprite = None
input_button_c = None
play_button_c = None
scoreboard_button_c = None
customization_button_c = None
settings_button_c = None
quit_button_c = None

input_is_active = False
fields_focused = [True, False]
current_usernames = ["", ""]


def get_input_components(y_level, order, username="", is_focused=False):
    input_label = paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X - 300,
        px_y=y_level,
        layer=globals.LAYER_SHIFT + globals.TEXT_LAYER,
        align="center",
        text=f"Player {order}",
        font_size=40,
        color=(255, 255, 255),

        key=f"input_label{order}",
    )  # endregion
    input_field_bg = paint_api.mount_rect(  # region parameters
        px_x=globals.CENTER_X + 50,
        px_y=y_level,
        px_w=500,
        px_h=90,
        layer=globals.LAYER_SHIFT + globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key=f"input_field_bg{order}",
    )  # endregion
    input_field_text = paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X + 50,
        px_y=y_level,
        px_w=500,
        px_h=90,
        layer=globals.LAYER_SHIFT + globals.TEXT_LAYER,
        align="center",
        text=username if username else INPUT_PLACEHOLDER_TEXT,
        font_size=40,
        color=(255, 255, 0) if is_focused else (255, 255, 255),

        key=f"input_field_text{order}",
    )  # endregion

    return {
        "input_label": input_label,
        "input_field_bg": input_field_bg,
        "input_field_text": input_field_text,
    }


def focus(inputs, order):
    global fields_focused

    for (cur_order, components) in enumerate(inputs):
        input_field_text = components["input_field_text"]
        if cur_order == order:
            input_field_text.set_color((255, 255, 0))
            fields_focused[cur_order] = True
        else:
            input_field_text.set_color((255, 255, 255))
            fields_focused[cur_order] = False


def render_input():
    global input_is_active, fields_focused, current_usernames

    bg_overlay = paint_api.mount_rect(  # region parameters
        px_x=0,
        px_y=0,
        px_w=globals.SCREEN_WIDTH,
        px_h=globals.SCREEN_HEIGHT,
        layer=globals.LAYER_SHIFT - 1,
        image_path="assets/images/backgrounds/overlay.png",

        key="bg_overlay"
    )  # endregion

    inputs = [
        get_input_components(globals.CENTER_Y - 120, 1, current_usernames[0], True),
        get_input_components(globals.CENTER_Y, 2, current_usernames[1])
    ]

    back_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 300,
        px_w=350,
        px_h=80,
        popup_layer=1,
        text="Back",
        font_size=50,

        key="back",
    )  # endregion

    if is_pressed_once(K_RETURN) or are_clicked(*back_button_c):
        input_is_active = False
        bg_overlay.unmount()

        for components in inputs:
            for component in components.values():
                component.unmount()

        fields_focused = [True, False]

        for component in back_button_c:
            component.unmount()
        return

    for (order, components) in enumerate(inputs):
        input_label = components["input_label"]
        input_field_bg = components["input_field_bg"]
        input_field_text = components["input_field_text"]
        if are_clicked(input_field_bg, input_field_text, input_label):
            focus(inputs, order)

        last_pressed_char = get_last_pressed_char()
        if fields_focused[order]:
            current_username = current_usernames[order]
            current_text = INPUT_PLACEHOLDER_TEXT
            updated = False

            if get_last_pressed_key() == K_BACKSPACE:
                if current_username:
                    current_username = current_username[:-1]
                    updated = True
            elif last_pressed_char:
                if len(current_username) < globals.MAX_USERNAME_LENGTH:
                    current_username += last_pressed_char
                    updated = True

            if current_username:
                current_text = current_username

            current_usernames[order] = current_username

            globals.usernames = current_usernames
            input_field_text.set_text(current_text)
            if updated:
                save_config()


def render_menu():
    global mute_button_sprite
    global input_button_c, play_button_c, scoreboard_button_c, customization_button_c, settings_button_c, quit_button_c

    mute_button_sprite = paint_api.mount_rect(  # region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y - 200,
        px_w=65,
        px_h=65,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path=globals.MUTED_IMG_PATH1 if globals.music_muted else globals.UNMUTED_IMG_PATH1,

        key="mute",
    )  # endregion

    input_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X + 345,
        px_y=40,
        px_w=100,
        px_h=65,
        text="Login",
        font_size=30,

        key="input",
    )  # endregion

    play_button_c = mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 100,
        px_w=500,
        px_h=90,
        text="Play",
        font_size=50,

        key="play",
    )  # endregion

    customization_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y,
        px_w=500,
        px_h=90,
        text="Customization",
        font_size=50,

        key="customization",
    )  # endregion

    settings_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X - 128,
        px_y=globals.CENTER_Y + 200,
        px_w=246,
        px_h=90,
        text="Settings",
        font_size=50,

        key="settings",
    )  # endregion

    scoreboard_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 100,
        px_w=500,
        px_h=90,
        text="Scoreboard",
        font_size=50,

        key="scoreboard",
    )  # endregion

    quit_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X + 128,
        px_y=globals.CENTER_Y + 200,
        px_w=246,
        px_h=90,
        text="Quit",
        font_size=50,

        key="quit",
    )  # endregion


def menu(is_setup=False):
    global mute_button_sprite
    global input_button_c, play_button_c, scoreboard_button_c, customization_button_c, settings_button_c, quit_button_c
    global input_is_active, current_usernames

    if is_setup:
        load_config()
        play_menu_music(volume=.2)
        paint_api.reset_frame()

        current_usernames = globals.usernames
        render_menu()

    if input_is_active:
        render_input()

    if are_clicked(*play_button_c):
        navigate("menu/play")
    elif are_clicked(*settings_button_c):
        navigate("menu/settings")
    elif are_clicked(*scoreboard_button_c):
        navigate("menu/scoreboard")
    elif are_clicked(*customization_button_c):
        navigate("menu/customization")
    elif are_clicked(*quit_button_c):
        sys.exit()

    if is_clicked(mute_button_sprite):
        if globals.music_muted:
            globals.music_muted = False
            play_menu_music(volume=.2)
            mute_button_sprite.set_image_path(globals.UNMUTED_IMG_PATH1)
        else:
            globals.music_muted = True
            stop_music()
            mute_button_sprite.set_image_path(globals.MUTED_IMG_PATH1)
        save_config()

    if are_clicked(*input_button_c):
        input_is_active = True
