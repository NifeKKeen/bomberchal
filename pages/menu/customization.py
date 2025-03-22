import configparser
import globals
import os
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked


CONFIG_FILE = "pages/menu/config.ini"

show_popup_window_p1 = False
show_popup_window_p2 = False
def load_config():
    if not os.path.exists(CONFIG_FILE):
        globals.skin_p1_id = 1
        globals.skin_p2_id = 2
        return
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if "Skin" in config:
        globals.skin_p1_id = config.getint("Skin", "skin_p1_id", fallback=1)
        globals.skin_p2_id = config.getint("Skin", "skin_p2_id", fallback=2)
    else:
        globals.skin_p1_id = 1
        globals.skin_p2_id = 2

def save_skin_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    if "Skin" not in config:
        config["Skin"] = {}
    config["Skin"]["skin_p1_id"] = str(globals.skin_p1_id)
    config["Skin"]["skin_p2_id"] = str(globals.skin_p2_id)
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def get_available_skin(current_skin, other_skin, delta):
    candidate = (current_skin + delta - 1) % len(globals.skins) + 1
    while candidate == other_skin:
        candidate = (candidate + delta - 1) % len(globals.skins) + 1
    return candidate

def pop_up_window():
    global show_popup_window_p1, show_popup_window_p2
    if show_popup_window_p1:
        idx = globals.skin_p1_id
    else:
        idx = globals.skin_p2_id
    demo_gif = paint_api.mount_gif(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 60,
        px_w=280,
        px_h=280,
        layer=globals.BUTTON_LAYER + globals.LAYER_SHIFT,
        align="center",
        delay=1000,
        frames=[f"assets/images/characters/ch{idx}/{direction}.png"
                for direction in ["up", "right", "down", "left"]],

        key="demo_gif",
        # layer=10  # ниже, чем кнопка закрытия
    )  #endregion

    close_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 110,
        px_w=50,
        px_h=50,
        layer=globals.BUTTON_LAYER + globals.LAYER_SHIFT,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="close_popup",
    )  #endregion
    close_pos = close_button.px_x, close_button.px_y
    close_button_text = paint_api.mount_text(  #region parameters
        px_x=close_pos[0],
        px_y=close_pos[1],
        layer=globals.TEXT_LAYER + globals.LAYER_SHIFT,
        align="center",
        text="x",
        font_size=30,
        color=(255, 255, 255),

        key="close_text",
    )  #endregion
    close_button_shadow = paint_api.mount_text(  #region parameters
        px_x=close_pos[0] + globals.SHADOW_OFFSET,
        px_y=close_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER + globals.LAYER_SHIFT,
        align="center",
        text="x",
        font_size=30,
        color=globals.SHADOW_COLOR,

        key="close_text_shadow",
    )  #endregion

    if is_clicked(close_button):
        print("close clicked")
        show_popup_window_p1 = False
        show_popup_window_p2 = False
        demo_gif.unmount()
        close_button.unmount()
        close_button_shadow.unmount()
        close_button_text.unmount()


def menu_customization():
    global player_skins, show_popup_window
    player_skins = globals.skins
    skin_display_index = 1

    global show_popup_window_p1
    global show_popup_window_p2
    load_config()

    paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 300,
        layer=globals.TEXT_LAYER,
        align="center",
        text="Change skin",
        font_size=40,
        color=(255, 255, 255),

        key="Customization_text",
    )  #endregion
    paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y - 170,
        layer=globals.TEXT_LAYER,
        text="for player1",
        font_size=30,
        color=(255, 255, 255),

        key="label_p1",
    )  #endregion

    left_arrow_p1 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 185,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/left.png",

        key="left_arrow_p1",
    )  #endregion
    right_arrow_p1 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y - 185,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/right.png",

        key="right_arrow_p1",
    )  #endregion
    preview_button_p1 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 225,
        px_y=globals.CENTER_Y - 230,
        px_w=150,
        px_h=50,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="skin_preview_p1",
    )  #endregion
    preview_pos_p1 = preview_button_p1.px_x, preview_button_p1.px_y
    preview_button_shadow_p1 = paint_api.mount_text(  #region parameters
        px_x=preview_pos_p1[0] + globals.SHADOW_OFFSET,
        px_y=preview_pos_p1[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text="Preview",
        font_size=30,
        color=globals.SHADOW_COLOR,

        key="preview_text_shadow_p1",
    )  #endregion
    preview_button_text_p1 = paint_api.mount_text(  #region parameters
        px_x=preview_pos_p1[0],
        px_y=preview_pos_p1[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="Preview",
        font_size=30,
        color=(255, 255, 255),

        key="preview_text_p1",
    )  #endregion

    display_p1 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 40,
        px_y=globals.CENTER_Y - 230,
        px_w=160,
        px_h=160,
        layer=globals.BUTTON_LAYER,
        # align="center",

        # image_path="assets/gifs/ch1/1.png",
        key="display_p1",
        image_path=globals.skins[f"ch{globals.skin_p1_id}"],
    )  #endregion

    paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y + 50,
        layer=globals.TEXT_LAYER,
        text="for player2",
        font_size=30,
        color=(255, 255, 255),

        key="label_p2_skin",
    )  #endregion
    left_arrow_p2 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y + 30,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/left.png",

        key="left_arrow_p2_skin",
    )  #endregion
    display_p2 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 40,
        px_y=globals.CENTER_Y + 10,
        px_w=160,
        px_h=160,
        layer=globals.BUTTON_LAYER,
        image_path=globals.skins[f"ch{globals.skin_p2_id}"],

        key="display_p2",
    )  #endregion
    right_arrow_p2 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y + 30,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/right.png",

        key="right_arrow_p2_skin",
    )  #endregion

    preview_button_p2 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y - 20 ,
        px_w=150,
        px_h=50,
        key="skin_preview_p2",
        image_path="assets/images/buttons/bar_button.png",
    )  #endregion
    preview_center_p2 = preview_button_p2.rect.center
    preview_button_shadow_p2 = paint_api.mount_text(  #region parameters
        px_x=preview_center_p2[0] + 4,
        px_y=preview_center_p2[1] + 4,
        key="preview_text_shadow_p2",
        text="Preview",
        font_size=30,
        color=(0, 0, 0),
        align="center",
    )  #endregion
    preview_button_text_p2 = paint_api.mount_text(  #region parameters
        px_x=preview_center_p2[0],
        px_y=preview_center_p2[1],
        key="preview_text_p2",
        text="Preview",
        font_size=30,
        color=(255, 255, 255),
        align="center",
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

    one_is_opened = show_popup_window_p1 or show_popup_window_p2
    if show_popup_window_p1 == 0 and show_popup_window_p2 == 0:
        if is_clicked(preview_button_p1):
            show_popup_window_p1 = True
        if is_clicked(preview_button_p2):
            show_popup_window_p2 = True
    if show_popup_window_p1 or show_popup_window_p2:
        pop_up_window()


    if not one_is_opened and (is_clicked(left_arrow_p1) or is_clicked(right_arrow_p1)):
        ind = -1 if is_clicked(left_arrow_p1) else 1
        globals.skin_p1_id = get_available_skin(globals.skin_p1_id, globals.skin_p2_id, ind)
        display_p1.set_image_path(globals.skins[f"ch{globals.skin_p1_id}"])
        save_skin_config()

    if not one_is_opened and (is_clicked(left_arrow_p2) or is_clicked(right_arrow_p2)):
        ind = -1 if is_clicked(left_arrow_p2) else 1
        globals.skin_p2_id = get_available_skin(globals.skin_p2_id, globals.skin_p1_id, ind)
        display_p2.set_image_path(globals.skins[f"ch{globals.skin_p2_id}"])
        save_skin_config()

    if not one_is_opened and is_clicked(back_button):
        navigate("menu")
