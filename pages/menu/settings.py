import pygame
import configparser
import globals
import os
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked, get_last_pressed_key
from utils.sound_api import play_menu_music

CONFIG_FILE = "pages/menu/config.ini"
def load_config():
    if not os.path.exists(CONFIG_FILE):
        globals.game_mode = "default"
        return
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if "Controls" in config:
        key1_str = config.get("Controls", "explosion_key_p1", fallback="space").strip()
        key2_str = config.get("Controls", "explosion_key_p2", fallback="m").strip()

        globals.controls_players[0]["explosion_key"] = parse_key(key1_str)
        globals.controls_players[1]["explosion_key"] = parse_key(key2_str)
    if "Game" in config:
        globals.game_mode = config.get("Game", "mode", fallback="default")  # исправлено: читаем ключ "mode"
    else:
        globals.game_mode = "default"

def parse_key(key_str):
    if key_str.lower() == "custom":
        return "custom"
    try:
        return int(key_str)  
    except ValueError:
        return pygame.key.key_code(key_str.lower())  


def save_config():
    config = configparser.ConfigParser()
    config["Controls"] = {
        "explosion_key_p1": str(globals.controls_players[0]["explosion_key"]),
        "explosion_key_p2": str(globals.controls_players[1]["explosion_key"])
    }
    config["Game"] = {"mode": str(globals.game_mode)}
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def settings(is_setup = False):
    if is_setup:
        play_menu_music(volume=.2)

    load_config()
    offered_keys_p0 = [pygame.K_SPACE, pygame.K_v, pygame.K_x, "custom"]
    try:
        current_index0 = offered_keys_p0.index(globals.controls_players[0]["explosion_key"])
    except ValueError:
        current_index0 = len(offered_keys_p0) - 1
        
    waiting_for_key = globals.controls_players[0]["explosion_key"] == "custom"

    def update_display(text_sprite, player_index, waiting):
        key_val = globals.controls_players[player_index]["explosion_key"]
        display_text = "Press key..." if waiting else (pygame.key.name(key_val) if key_val != "custom" else "Custom")
        text_sprite.set_text(display_text)

    paint_api.mount_text(
        px_x=globals.center_x,
        px_y=globals.center_y - 250,
        key="change_bomb_button",
        text="Change bomb button",
        font_size=40,
        color=(255, 255, 255),
        align="center"
    )
    paint_api.mount_text(
        px_x=globals.center_x - 350,
        px_y=globals.center_y - 170,
        key="label_p0",
        text="for player1",
        font_size=30,
        color=(255, 255, 255)
    )

    left_arrow_p0 = paint_api.mount_rect(
        px_x=globals.center_x - 150,
        px_y=globals.center_y - 185,
        px_w=75,
        px_h=75,
        key="left_arrow_p0",
        image_path="assets/images/buttons/left.png",
    )
    current_key_text_p0 = "Custom" if offered_keys_p0[current_index0] == "custom" else pygame.key.name(offered_keys_p0[current_index0])
    display_p0 = paint_api.mount_text(
        px_x=globals.center_x + 35,
        px_y=globals.center_y - 150,
        key="display_p0",
        text=current_key_text_p0,
        font_size=25,
        color=(255, 255, 0),
        align="center"
    )
    right_arrow_p0 = paint_api.mount_rect(
        px_x=globals.center_x + 150,
        px_y=globals.center_y - 185,
        px_w=75,
        px_h=75,
        key="right_arrow_p0",
        image_path="assets/images/buttons/right.png",
    )
    if is_clicked(left_arrow_p0) or is_clicked(right_arrow_p0):
        new_index0 = (current_index0 + (-1 if is_clicked(left_arrow_p0) else 1)) % len(offered_keys_p0)
        new_key0 = offered_keys_p0[new_index0]
        if new_key0 != "custom" and new_key0 == globals.controls_players[1]["explosion_key"]:
            display_p0.set_text("Duplicate!")
        else:
            if new_key0 == "custom":
                globals.controls_players[0]["explosion_key"] = "custom"
                waiting_for_key = True
            else:
                globals.controls_players[0]["explosion_key"] = new_key0
                waiting_for_key = False
            update_display(display_p0, 0, waiting_for_key)
            save_config()
    if waiting_for_key:
        pressed_key = get_last_pressed_key()
        if pressed_key is not None:
            if pressed_key == globals.controls_players[1]["explosion_key"]:
                display_p0.set_text("Duplicate!")
            else:
                globals.controls_players[0]["explosion_key"] = pressed_key
                waiting_for_key = False
                update_display(display_p0, 0, waiting_for_key)
                save_config()

    offered_keys_p1 = [pygame.K_RETURN, pygame.K_m, pygame.K_n, "custom"]
    try:
        current_index1 = offered_keys_p1.index(globals.controls_players[1]["explosion_key"])
    except ValueError:
        current_index1 = len(offered_keys_p1) - 1

    waiting_for_key2 = globals.controls_players[1]["explosion_key"] == "custom"

    paint_api.mount_text(
        px_x=globals.center_x - 350,
        px_y=globals.center_y - 50,  
        key="label_p1",
        text="for player2",
        font_size=30,
        color=(255, 255, 255),
    )

    left_arrow_p1 = paint_api.mount_rect(
        px_x=globals.center_x - 150,
        px_y=globals.center_y - 65,  
        px_w=75,
        px_h=75,
        key="left_arrow_p1",
        image_path="assets/images/buttons/left.png",
    )
    current_key_text_p1 = "Custom" if offered_keys_p1[current_index1] == "custom" else pygame.key.name(offered_keys_p1[current_index1])
    display_p1 = paint_api.mount_text(
        px_x=globals.center_x + 35,
        px_y=globals.center_y - 35, 
        key="display_p1",
        text=current_key_text_p1,
        font_size=25,
        color=(255, 255, 0),
        align = "center"
    )
    right_arrow_p1 = paint_api.mount_rect(
        px_x=globals.center_x + 150,
        px_y=globals.center_y - 65, 
        px_w=75,
        px_h=75,
        key="right_arrow_p1",
        image_path="assets/images/buttons/right.png",
    )
    if is_clicked(left_arrow_p1) or is_clicked(right_arrow_p1):
        new_index1 = (current_index1 + (-1 if is_clicked(left_arrow_p1) else 1)) % len(offered_keys_p1)
        new_key1 = offered_keys_p1[new_index1]
        if new_key1 != "custom" and new_key1 == globals.controls_players[0]["explosion_key"]:
            display_p1.set_text("Duplicate!")
        else:
            if new_key1 == "custom":
                globals.controls_players[1]["explosion_key"] = "custom"
                waiting_for_key2 = True
            else:
                globals.controls_players[1]["explosion_key"] = new_key1
                waiting_for_key2 = False
            update_display(display_p1, 1, waiting_for_key2)
            save_config()
    if waiting_for_key2:
        pressed_key = get_last_pressed_key()
        if pressed_key is not None:
            if pressed_key == globals.controls_players[0]["explosion_key"]:
                display_p1.set_text("Duplicate!")
            else:
                globals.controls_players[1]["explosion_key"] = pressed_key
                waiting_for_key2 = False
                update_display(display_p1, 1, waiting_for_key2)
                save_config()

    
    paint_api.mount_text(
        px_x=globals.center_x - 350,
        px_y=globals.center_y + 50,  
        key="game_mode",
        text="Game mode",
        font_size=30,
        color=(255, 255, 255),
    )

    default_button = paint_api.mount_rect(
        px_x=globals.center_x - 130,
        px_y=globals.center_y + 40,
        px_w=170,
        px_h=60,
        key="default",
        image_path="assets/images/buttons/bar_button.png",
    )
    default_center = default_button.rect.center
    default_button_shadow = paint_api.mount_text(
        px_x=default_center[0] + 4,
        px_y=default_center[1] + 4,
        key="default_text_shadow",
        text="Default",
        font_size=40,
        color=(0, 0, 0),
        align="center"
    )
    default_button_text = paint_api.mount_text(
        px_x=default_center[0],
        px_y=default_center[1],
        key="default_text",
        text="Default",
        font_size=40,
        color=(255, 255, 255),
        align="center"
    )
    boss_button = paint_api.mount_rect(
        px_x=globals.center_x + 70,
        px_y=globals.center_y + 40,
        px_w=250,
        px_h=60,
        key="boss",
        image_path="assets/images/buttons/bar_button.png",
    )
    boss_center = boss_button.rect.center
    boss_button_shadow = paint_api.mount_text(
        px_x=boss_center[0] + 4,
        px_y=boss_center[1] + 4,
        key="boss_text_shadow",
        text="Boss Fight",
        font_size=40,
        color=(0, 0, 0),
        align="center"
    )
    boss_button_text = paint_api.mount_text(
        px_x=boss_center[0],
        px_y=boss_center[1],
        key="boss_text",
        text="Boss Fight",
        font_size=40,
        color=(255, 255, 255),
        align="center"
    )
      
    if is_clicked(default_button):
        globals.game_mode = "default"
        print("default clicked")
        save_config()
    if is_clicked(boss_button):
        print("boss clicked")
        globals.game_mode = "bossfight"
        save_config()

    if globals.game_mode == "default":
        print("default")
        default_button_text.set_color((255, 255, 0)) 
        boss_button_text.set_color((255, 255, 255))     
    elif (globals.game_mode == "bossfight"):
        print()
        boss_button_text.set_color((255, 255, 0))        
        default_button_text.set_color((255, 255, 255))      

    back_button = paint_api.mount_rect(
        px_y=globals.center_y + 300,
        px_w=350,
        px_h=80,
        key="back",
        image_path="assets/images/buttons/bar_button.png",
        align="center"
    )
    back_center = back_button.rect.center
    back_button_shadow = paint_api.mount_text(
        px_x=back_center[0] + 4,
        px_y=back_center[1] + 4,
        key="back_text_shadow",
        text="Back",
        font_size=50,
        color=(0, 0, 0),
        align="center"
    )
    back_button_text = paint_api.mount_text(
        px_x=back_center[0],
        px_y=back_center[1],
        key="back_text",
        text="Back",
        font_size=50,
        color=(255, 255, 255),
        align = "center"
    )

    
    if is_clicked(back_button):
        if globals.controls_players[0]["explosion_key"] == "custom":
            globals.controls_players[0]["explosion_key"] = pygame.K_SPACE
        if globals.controls_players[1]["explosion_key"] == "custom":
            globals.controls_players[1]["explosion_key"] = pygame.K_RETURN
        save_config()
        navigate("menu")
