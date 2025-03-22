import pygame
import configparser
import globals
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked


def menu_scoreboard():
    paint_api.mount_text(
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 300,
        key="change_bomb_button",
        text="Scoreboard",
        font_size=40,
        color=(255, 255, 255),
        align="center"
    )
    #something

    back_button = paint_api.mount_rect(
        px_y=globals.CENTER_Y + (globals.CENTER_Y // 2),
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