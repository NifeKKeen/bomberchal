import pygame
import globals
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked

def menu_scoreboard():
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
    #something
    for index, score in enumerate():
        paint_api.mount_text(  #region parameters
            px_x=globals.CENTER_X,
            px_y=globals.CENTER_Y - 250 + index * 50,
            layer=globals.TEXT_LAYER,
            align="center",
            text=f"{index + 1}. {score}",
            font_size=30,
            color=(255, 255, 255),
            key=f"score_{index}",
        )  #endregion
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