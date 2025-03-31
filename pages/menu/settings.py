import globals
import pygame
from config import load_config, save_config
from pages.navigation import navigate
from utils import paint_api
from utils.interaction_api import is_clicked, get_last_pressed_key, are_clicked
from utils.sound_api import play_menu_music, play_button_click


def update_display(text_sprite, player_index, waiting):
    key_val = globals.controls_players[player_index]["explosion_key"]
    display_text = "Press key..." if waiting else (pygame.key.name(key_val) if key_val != "custom" else "Custom")
    text_sprite.set_text(display_text)


left_arrow_p1 = None
display_p1 = None
right_arrow_p1 = None
left_arrow_p2 = None
display_p2 = None
right_arrow_p2 = None
back_button_c = None
bomb_mute_button_sprite = None

current_key_text_p1 = None
current_key_text_p2 = None


def render_settings():
    global left_arrow_p1, display_p1, right_arrow_p1
    global left_arrow_p2, display_p2, right_arrow_p2
    global back_button_c
    global current_key_text_p1, current_key_text_p2
    global bomb_mute_button_sprite

    paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 250,
        layer=globals.TEXT_LAYER,
        align="center",
        text="Change bomb button",
        font_size=40,
        color=(255, 255, 255),

        key="change_bomb_button",
    )  # endregion
    paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y - 170,
        layer=globals.TEXT_LAYER,
        text="for player1",
        font_size=30,
        color=(255, 255, 255),

        key="label_p1",
    )  # endregion

    left_arrow_p1 = paint_api.mount_rect(  # region parameters
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 185,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/left.png",

        key="left_arrow_p1",
    )  # endregion
    display_p1 = paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X + 35,
        px_y=globals.CENTER_Y - 150,
        layer=globals.TEXT_LAYER,
        align="center",
        text=current_key_text_p1,
        font_size=25,
        color=(255, 255, 0),

        key="display_p1",
    )  # endregion
    right_arrow_p1 = paint_api.mount_rect(  # region parameters
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y - 185,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/right.png",

        key="right_arrow_p1",
    )  # endregion

    paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y - 50,
        layer=globals.TEXT_LAYER,
        text="for player2",
        font_size=30,
        color=(255, 255, 255),

        key="label_p2",
    )  # endregion

    left_arrow_p2 = paint_api.mount_rect(  # region parameters
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 65,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/left.png",

        key="left_arrow_p2",
    )  # endregion
    display_p2 = paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X + 35,
        px_y=globals.CENTER_Y - 35,
        layer=globals.TEXT_LAYER,
        align="center",
        text=current_key_text_p2,
        font_size=25,
        color=(255, 255, 0),

        key="display_p2",
    )  # endregion
    right_arrow_p2 = paint_api.mount_rect(  # region parameters
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y - 65,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/right.png",

        key="right_arrow_p2",
    )  # endregion

    paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y + 150,
        layer=globals.TEXT_LAYER,
        text="Mute bomb sound",
        font_size=30,
        color=(255, 255, 255),

        key="bomb_mute_text",
    )  # endregion
    bomb_mute_button_sprite = paint_api.mount_rect(  # region parameters
        px_x=globals.CENTER_X + 20,
        px_y=globals.CENTER_Y + 165,
        px_w=65,
        px_h=65,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path=globals.MUTED_IMG_PATH2 if globals.sound_muted else globals.UNMUTED_IMG_PATH2,

        key="bomb_mute",
    )  # endregion

    back_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 300,
        px_w=350,
        px_h=80,
        text="Back",
        font_size=50,

        key="back",
    )  # endregion


def settings(is_setup=False):
    global left_arrow_p1, display_p1, right_arrow_p1
    global left_arrow_p2, display_p2, right_arrow_p2
    global back_button_c
    global current_key_text_p1, current_key_text_p2

    load_config()
    offered_keys_p1 = [pygame.K_SPACE, pygame.K_v, pygame.K_x, "custom"]
    try:
        current_index0 = offered_keys_p1.index(globals.controls_players[0]["explosion_key"])
    except ValueError:
        current_index0 = len(offered_keys_p1) - 1

    waiting_for_key1 = globals.controls_players[0]["explosion_key"] == "custom"

    current_key_text_p1 = "Custom" if offered_keys_p1[current_index0] == "custom" else pygame.key.name(offered_keys_p1[current_index0])

    offered_keys_p2 = [pygame.K_RETURN, pygame.K_m, pygame.K_n, "custom"]
    try:
        current_index1 = offered_keys_p2.index(globals.controls_players[1]["explosion_key"])
    except ValueError:
        current_index1 = len(offered_keys_p2) - 1

    waiting_for_key2 = globals.controls_players[1]["explosion_key"] == "custom"

    current_key_text_p2 = "Custom" if offered_keys_p2[current_index1] == "custom" else pygame.key.name(offered_keys_p2[current_index1])

    if is_setup:
        play_menu_music(volume=.2)
        render_settings()

    if is_clicked(left_arrow_p1) or is_clicked(right_arrow_p1):
        play_button_click()
        new_index0 = (current_index0 + (-1 if is_clicked(left_arrow_p1) else 1)) % len(offered_keys_p1)
        new_key0 = offered_keys_p1[new_index0]
        if new_key0 != "custom" and new_key0 == globals.controls_players[1]["explosion_key"]:
            display_p1.set_text("Duplicate!")
        else:
            if new_key0 == "custom":
                globals.controls_players[0]["explosion_key"] = "custom"
                waiting_for_key1 = True
            else:
                globals.controls_players[0]["explosion_key"] = new_key0
                waiting_for_key1 = False
            update_display(display_p1, 0, waiting_for_key1)
            save_config()
    if waiting_for_key1:
        pressed_key = get_last_pressed_key()
        if pressed_key is not None:
            if pressed_key == globals.controls_players[1]["explosion_key"]:
                display_p1.set_text("Duplicate!")
            else:
                globals.controls_players[0]["explosion_key"] = pressed_key
                waiting_for_key1 = False
                update_display(display_p1, 0, waiting_for_key1)
                save_config()

    if is_clicked(left_arrow_p2) or is_clicked(right_arrow_p2):
        play_button_click()
        new_index1 = (current_index1 + (-1 if is_clicked(left_arrow_p2) else 1)) % len(offered_keys_p2)
        new_key1 = offered_keys_p2[new_index1]
        if new_key1 != "custom" and new_key1 == globals.controls_players[0]["explosion_key"]:
            display_p2.set_text("Duplicate!")
        else:
            if new_key1 == "custom":
                globals.controls_players[1]["explosion_key"] = "custom"
                waiting_for_key2 = True
            else:
                globals.controls_players[1]["explosion_key"] = new_key1
                waiting_for_key2 = False
            update_display(display_p2, 1, waiting_for_key2)
            save_config()
    if waiting_for_key2:
        pressed_key = get_last_pressed_key()
        if pressed_key is not None:
            if pressed_key == globals.controls_players[0]["explosion_key"]:
                display_p2.set_text("Duplicate!")
            else:
                globals.controls_players[1]["explosion_key"] = pressed_key
                waiting_for_key2 = False
                update_display(display_p2, 1, waiting_for_key2)
                save_config()

    if is_clicked(bomb_mute_button_sprite):
        play_button_click()
        if globals.sound_muted:
            globals.sound_muted = False
            bomb_mute_button_sprite.set_image_path(globals.UNMUTED_IMG_PATH2)
        else:
            globals.sound_muted = True
            bomb_mute_button_sprite.set_image_path(globals.MUTED_IMG_PATH2)
        save_config()
            
    if are_clicked(*back_button_c):
        play_button_click()
        if globals.controls_players[0]["explosion_key"] == "custom":
            globals.controls_players[0]["explosion_key"] = pygame.K_SPACE
        if globals.controls_players[1]["explosion_key"] == "custom":
            globals.controls_players[1]["explosion_key"] = pygame.K_RETURN
        save_config()
        navigate("menu")
