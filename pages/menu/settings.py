import pygame
import configparser
import globals
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked, get_last_pressed_key

CONFIG_FILE = "pages/menu/config.ini"
def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if "Controls" in config:
        key1_str = config.get("Controls", "explosion_key_p1", fallback="space").strip()
        key2_str = config.get("Controls", "explosion_key_p2", fallback="m").strip()

        globals.controls_players[0]["explosion_key"] = parse_key(key1_str)
        globals.controls_players[1]["explosion_key"] = parse_key(key2_str)

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
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def settings(is_setup = False):
    if is_setup:
        if globals.current_music != globals.menu_music_path:
            globals.current_music = globals.menu_music_path
            pygame.mixer.music.load(globals.menu_music_path)
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(-1)

    load_config()
    offered_keys_p0 = [pygame.K_SPACE, pygame.K_v, pygame.K_x, "custom"]
    try:
        current_index0 = offered_keys_p0.index(globals.controls_players[0]["explosion_key"])
    except ValueError:
        current_index0 = len(offered_keys_p0) - 1
        
    waiting_for_key = globals.controls_players[0]["explosion_key"] == "custom"

    def update_display():
        key_val = globals.controls_players[0]["explosion_key"]
        display_text = "Press key..." if waiting_for_key else pygame.key.name(key_val)
        paint_api.update_text("display_p0", text=display_text)

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
    current_key_text_p0 = pygame.key.name(
        offered_keys_p0[current_index0] 
        if offered_keys_p0[current_index0] != "custom" 
        else pygame.K_0
    )
    display_p0 = paint_api.mount_text(
        px_x=globals.center_x ,
        px_y=globals.center_y - 170,
        key="display_p0",
        text=current_key_text_p0,
        font_size=25,
        color=(255, 255, 0)
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
        if new_key0 == "custom":
            globals.controls_players[0]["explosion_key"] = "custom"
            waiting_for_key = True
        else:
            globals.controls_players[0]["explosion_key"] = new_key0
            waiting_for_key = False
        update_display()
        save_config()  
    if waiting_for_key:
        pressed_key = get_last_pressed_key()
        if pressed_key is not None:
            globals.controls_players[0]["explosion_key"] = pressed_key
            waiting_for_key = False
            update_display()
            save_config()

    offered_keys_p1 = [pygame.K_RETURN, pygame.K_m, pygame.K_n, "custom"]
    try:
        current_index1 = offered_keys_p1.index(globals.controls_players[1]["explosion_key"])
    except ValueError:
        current_index1 = len(offered_keys_p1) - 1

    waiting_for_key2 = globals.controls_players[1]["explosion_key"] == "custom"

    def update_display2():
        key_val = globals.controls_players[1]["explosion_key"]
        display_text = "Press key..." if waiting_for_key2 else pygame.key.name(key_val)
        paint_api.update_text("display_p1", text=display_text)

    paint_api.mount_text(
        px_x=globals.center_x - 350,
        px_y=globals.center_y + 25,  
        key="label_p1",
        text="for player2",
        font_size=30,
        color=(255, 255, 255)
    )

    left_arrow_p1 = paint_api.mount_rect(
        px_x=globals.center_x - 150,
        px_y=globals.center_y + 15,  
        px_w=75,
        px_h=75,
        key="left_arrow_p1",
        image_path="assets/images/buttons/left.png",
    )
    current_key_text_p1 = pygame.key.name(
        offered_keys_p1[current_index1]
        if offered_keys_p1[current_index1] != "custom"
        else pygame.K_0
    )
    display_p1 = paint_api.mount_text(
        px_x=globals.center_x,
        px_y=globals.center_y + 25, 
        key="display_p1",
        text=current_key_text_p1,
        font_size=25,
        color=(255, 255, 0)
    )
    right_arrow_p1 = paint_api.mount_rect(
        px_x=globals.center_x + 150,
        px_y=globals.center_y + 15, 
        px_w=75,
        px_h=75,
        key="right_arrow_p1",
        image_path="assets/images/buttons/right.png",
    )
    if is_clicked(left_arrow_p1) or is_clicked(right_arrow_p1):
        new_index1 = (current_index1 + (-1 if is_clicked(left_arrow_p1) else 1)) % len(offered_keys_p1)
        new_key1 = offered_keys_p1[new_index1]
        if new_key1 == "custom":
            globals.controls_players[1]["explosion_key"] = "custom"
            waiting_for_key2 = True
        else:
            globals.controls_players[1]["explosion_key"] = new_key1
            waiting_for_key2 = False
        update_display2()
        save_config()
    if waiting_for_key2:
        pressed_key = get_last_pressed_key()
        if pressed_key is not None:
            globals.controls_players[1]["explosion_key"] = pressed_key
            waiting_for_key2 = False
            update_display2()
            save_config()


    back_button = paint_api.mount_rect(
        px_y=globals.center_y + (globals.center_y // 2),
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
        color=(0, 0, 0)
    )
    back_button_text = paint_api.mount_text(
        px_x=back_center[0],
        px_y=back_center[1],
        key="back_text",
        text="Back",
        font_size=50,
        color=(255, 255, 255)
    )
    back_button_text.rect.center = back_center
    back_button_shadow.rect.center = (back_center[0] + 4, back_center[1] + 4)
    if is_clicked(back_button):
        navigate("menu")
