import pygame
import configparser
import globals
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked, get_pressed_key

CONFIG_FILE = "settings.ini"

def save_settings():
    config = configparser.ConfigParser()
    config["CONTROLS"] = {
        "player1_explosion_key": str(globals.controls_players[0]["explosion_key"])
    }
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def load_settings():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if "CONTROLS" in config:
        globals.controls_players[0]["explosion_key"] = int(config["CONTROLS"].get("player1_explosion_key", pygame.K_SPACE))

def settings():
    offered_keys_p0 = [pygame.K_SPACE, pygame.K_a, pygame.K_m, "custom"]
    try:
        current_index0 = offered_keys_p0.index(globals.controls_players[0]["explosion_key"])
    except ValueError:
        current_index0 = len(offered_keys_p0) - 1

    def update_display():
        key_val = globals.controls_players[0]["explosion_key"]
        if key_val is None:
            key_val = pygame.K_SPACE  
        current_key_text_p0 = pygame.key.name(key_val)
        paint_api.update_text("display_p0", text=current_key_text_p0)

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
        px_w=64,
        px_h=64,
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
        font_size=20,
        color=(255, 255, 0)
    )
    right_arrow_p0 = paint_api.mount_rect(
        px_x=globals.center_x + 150,
        px_y=globals.center_y - 185,
        px_w=64,
        px_h=64,
        key="right_arrow_p0",
        image_path="assets/images/buttons/right.png",
    )
    if is_clicked(left_arrow_p0):
        new_index0 = (current_index0 - 1) % len(offered_keys_p0)
        new_key0 = offered_keys_p0[new_index0]
        if new_key0 == "custom":
            new_key0 = get_pressed_key()  # ожидаем ввод с таймаутом
        globals.controls_players[0]["explosion_key"] = new_key0
        update_display()
        print("Player1 bomb key:", globals.controls_players[0]["explosion_key"])
        save_settings()
    if is_clicked(right_arrow_p0):
        new_index0 = (current_index0 + 1) % len(offered_keys_p0)
        new_key0 = offered_keys_p0[new_index0]
        if new_key0 == "custom":
            new_key0 = get_pressed_key()  # ожидаем ввод с таймаутом
        globals.controls_players[0]["explosion_key"] = new_key0
        update_display()
        print("Player1 bomb key:", globals.controls_players[0]["explosion_key"])
        save_settings()

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
