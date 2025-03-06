import pygame
import configparser
import globals
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked, get_pressed_key

# Файл конфигурации
CONFIG_FILE = "pages/menu/settings.ini"

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

def load_settings():
    if not config.has_section("Controls"):
        config.add_section("Controls")
    globals.controls_players[0]["explosion_key"] = config.getint("Controls", "BombKeyPlayer1", fallback=pygame.K_SPACE)
    globals.controls_players[1]["explosion_key"] = config.getint("Controls", "BombKeyPlayer2", fallback=pygame.K_RETURN)

def save_settings():
    config.set("Controls", "BombKeyPlayer1", str(globals.controls_players[0]["explosion_key"]))
    config.set("Controls", "BombKeyPlayer2", str(globals.controls_players[1]["explosion_key"]))
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    print("Bomb Player 1 key: ", str(globals.controls_players[0]["explosion_key"]))
    print("Bomb Player 2 key: ", str(globals.controls_players[1]["explosion_key"]))

def settings():
    offered_keys_p0 = [pygame.K_SPACE, pygame.K_a, pygame.K_m, "custom"]
    offered_keys_p1 = [pygame.K_RETURN, pygame.K_SPACE, pygame.K_m, "custom"]
    
    for player_idx, offered_keys in enumerate([offered_keys_p0, offered_keys_p1]):
        try:
            current_index = offered_keys.index(globals.controls_players[player_idx]["explosion_key"])
        except ValueError:
            current_index = len(offered_keys) - 1
        
        left_arrow = paint_api.mount_rect(
            px_x=globals.center_x - 150,
            px_y=globals.center_y - 170 + (player_idx * 100),
            px_w=50,
            px_h=50,
            key=f"left_arrow_p{player_idx}",
        )
        
        current_key_text = pygame.key.name(
            offered_keys[current_index] if offered_keys[current_index] != "custom" else pygame.K_0
        )
        display = paint_api.mount_text(
            px_x=globals.center_x,
            px_y=globals.center_y - 0 + (player_idx * 100),
            key=f"display_p{player_idx}",
            text=current_key_text,
            font_size=20,
            color=(255, 255, 0)
        )
        
        right_arrow = paint_api.mount_rect(
            px_x=globals.center_x + 150,
            px_y=globals.center_y - 170 + (player_idx * 100),
            px_w=50,
            px_h=50,
            key=f"right_arrow_p{player_idx}",
        )
        
        if is_clicked(left_arrow):
            new_index = (current_index - 1) % len(offered_keys)
            new_key = offered_keys[new_index]
            if new_key == "custom":
                new_key = get_pressed_key()
            globals.controls_players[player_idx]["explosion_key"] = new_key
            save_settings()
        
        if is_clicked(right_arrow):
            new_index = (current_index + 1) % len(offered_keys)
            new_key = offered_keys[new_index]
            if new_key == "custom":
                new_key = get_pressed_key()
            globals.controls_players[player_idx]["explosion_key"] = new_key
            save_settings()
    
    back_button = paint_api.mount_rect(
        px_y=globals.center_y + (globals.center_y // 2),
        px_w=350,
        px_h=80,
        key="back",
        image_path="assets/images/buttons/bar_button.png",
        align="center"
    )
    if is_clicked(back_button):
        navigate("menu")

load_settings()
