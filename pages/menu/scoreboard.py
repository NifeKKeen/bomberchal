import pygame
import globals
from utils import paint_api  # изменено для использования scoreboard_api3
from pages.navigation import navigate
from utils.interaction_api import is_clicked
from utils import scoreboard_api as scoreboard_api

game_mode = "pve"

def menu_scoreboard():
    global game_mode
    paint_api.mount_text( #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 300,
        layer=globals.TEXT_LAYER,
        align="center",
        text="Scoreboard",
        font_size=40,
        color=(255, 255, 255),
        key="scoreboard_title",
    ) #endregion
    pve_sprite = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 250,
        px_y=globals.CENTER_Y - 200,
        px_w=150,
        px_h=80,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="pve",
    )  #endregion
    pve_pos = pve_sprite.px_x, pve_sprite.px_y
    pve_text = paint_api.mount_text(  #region parameters
        px_x=pve_pos[0],
        px_y=pve_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="PvE",
        font_size=50,
        color=(255, 255, 255),

        key="pve_text",
    )  #endregion
    pve_shadow = paint_api.mount_text(  #region parameters
        px_x=pve_pos[0] + globals.SHADOW_OFFSET,
        px_y=pve_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text="PvE",
        font_size=50,
        color=globals.SHADOW_COLOR,

        key="pve_shadow",
    )  #endregion
    duel_sprite = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 70,
        px_y=globals.CENTER_Y - 200,
        px_w=150,
        px_h=80,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="duel",
    )  #endregion
    duel_pos = duel_sprite.px_x, duel_sprite.px_y
    duel_text = paint_api.mount_text(  #region parameters
        px_x=duel_pos[0],
        px_y=duel_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="Duel",
        font_size=50,
        color=(255, 255, 255),

        key="duel_text",
    )  #endregion
    duel_shadow = paint_api.mount_text(  #region parameters
        px_x=duel_pos[0] + globals.SHADOW_OFFSET,
        px_y=duel_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text="Duel",
        font_size=50,
        color=globals.SHADOW_COLOR,

        key="duel_shadow",
    )  #endregion
    bossfight_sprite = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 190,
        px_y=globals.CENTER_Y - 200,
        px_w=300,
        px_h=80,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="bossfight",
    )  #endregion
    bossfight_pos = bossfight_sprite.px_x, bossfight_sprite.px_y
    bossfight_text = paint_api.mount_text(  #region parameters
        px_x=bossfight_pos[0],
        px_y=bossfight_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="bossfight",
        font_size=50,
        color=(255, 255, 255),

        key="bossfight_text",
    )  #endregion
    bossfight_shadow = paint_api.mount_text(  #region parameters
        px_x=bossfight_pos[0] + globals.SHADOW_OFFSET,
        px_y=bossfight_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text="bossfight",
        font_size=50,
        color=globals.SHADOW_COLOR,

        key="bossfight_shadow",
    )  #endregion

    if is_clicked(pve_sprite):
        game_mode = "pve"
    elif is_clicked(duel_sprite):
        game_mode = "duel"
    elif is_clicked(bossfight_sprite):
        game_mode = "bossfight"

    scoreboard_sprite = scoreboard_api.mount_scoreboard(
        game_mode, 
        px_x=globals.CENTER_X, 
        px_y=globals.CENTER_Y + 50,
        align="center",
        font_size=30,
        bg_color=(50, 50, 50, 180),  
    )  
    back_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 300,
        px_w=350,
        px_h=80,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="back",
    )  #endregion
    back_pos = back_button.px_x, back_button.px_y
    back_button_shadow = paint_api.mount_text(  #region parameters
        px_x=back_pos[0] + globals.SHADOW_OFFSET,
        px_y=back_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text="Back",
        font_size=50,
        color=globals.SHADOW_COLOR,

        key="back_text_shadow",
    )  #endregion
    back_button_text = paint_api.mount_text(  #region parameters
        px_x=back_pos[0],
        px_y=back_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="Back",
        font_size=50,
        color=(255, 255, 255),

        key="back_text",
    )  #endregion

    if is_clicked(back_button):
        navigate("menu")