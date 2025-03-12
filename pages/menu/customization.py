import pygame
import configparser
import globals
# import random              # добавлено для использования random.shuffle
from utils import paint_api
# from pages.navigation import navigate
# from utils.interaction_api import is_clicked

# CONFIG_FILE = "pages/menu/config.ini"

# def load_config():
#     config = configparser.ConfigParser()
#     config.read(CONFIG_FILE)


# def save_skins():
#     config["Skins"] = player_skins
#     with open("settings.ini", "w") as configfile:
#         config.write(configfile)

# def get_available_skins():
#     taken = set(player_skins.values())
#     return [s for s in SKINS if s not in taken]

# def assign_bot_skins():
#     available = get_available_skins()
#     random.shuffle(available)
#     return available

# bot_skins = assign_bot_skins()

# def change_skin(player, direction):
#     current_index = SKINS.index(player_skins[player])
#     available_skins = get_available_skins()
#     new_index = (current_index + direction) % len(SKINS)
#     while SKINS[new_index] not in available_skins:
#         new_index = (new_index + direction) % len(SKINS)
#     player_skins[player] = SKINS[new_index]


def menu_customization():
    
    player_skins = globals.player_skins


    paint_api.mount_text(
        px_x=globals.center_x,
        px_y=globals.center_y - 300,
        key="Customization_text",
        text="Customization",
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
#     left_arrow_p0 = paint_api.mount_rect(
#         px_x=globals.center_x - 150,
#         px_y=globals.center_y - 185,
#         px_w=75,
#         px_h=75,
#         key="left_arrow_p0",
#         image_path="assets/images/buttons/left.png",
#     )
#     right_arrow_p0 = paint_api.mount_rect(
#         px_x=globals.center_x + 150,
#         px_y=globals.center_y - 185,
#         px_w=75,
#         px_h=75,
#         key="right_arrow_p0",
#         image_path="assets/images/buttons/right.png",
#     )
    
#     # Добавляем логику для смены скина по стрелкам
#     if is_clicked(left_arrow_p0):
#         change_skin("player1", -1)
#     if is_clicked(right_arrow_p0):
#         change_skin("player1", 1)
    
#     # Отображение выбранного скина
#     skin_preview = paint_api.mount_image(
#         px_x=globals.center_x,
#         px_y=globals.center_y,
#         key="skin_preview",
#         image_path=f"assets/characters/{player_skins['player1']}.png",
#         align="center"
#     )
    
#     back_button = paint_api.mount_rect(
#         px_y=globals.center_y + (globals.center_y // 2),
#         px_w=350,
#         px_h=80,
#         key="back",
#         image_path="assets/images/buttons/bar_button.png",
#         align="center"
#     )
#     back_center = back_button.rect.center
#     back_button_shadow = paint_api.mount_text(
#         px_x=back_center[0] + 4,
#         px_y=back_center[1] + 4,
#         key="back_text_shadow",
#         text="Back",
#         font_size=50,
#         color=(0, 0, 0)
#     )
#     back_button_text = paint_api.mount_text(
#         px_x=back_center[0],
#         px_y=back_center[1],
#         key="back_text",
#         text="Back",
#         font_size=50,
#         color=(255, 255, 255)
#     )
#     back_button_text.rect.center = back_center
#     back_button_shadow.rect.center = (back_center[0] + 4, back_center[1] + 4)
#     if is_clicked(back_button):
#         navigate("menu")
