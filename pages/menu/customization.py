import configparser
import globals
import os
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked, are_clicked
from config import load_config


CONFIG_FILE = "config.ini"

show_popup_window_p1 = False
show_popup_window_p2 = False
show_popup_window = False
player_skins = None

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
    )  #endregion

    bg_overlay = paint_api.mount_rect(  #region parameters
        px_x=0,
        px_y=0,
        px_w=globals.SCREEN_WIDTH,
        px_h=globals.SCREEN_HEIGHT,
        layer=globals.LAYER_SHIFT - 1,
        image_path="assets/images/backgrounds/overlay.png",

        key="bg_overlay"
    )  #endregion

    close_button_c = paint_api.mount_button(  #region parameters
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 110,
        px_w=50,
        px_h=50,
        popup_layer=1,
        text="x",
        font_size=30,

        key="close_popup",
    )  #endregion

    if are_clicked(*close_button_c):
        show_popup_window_p1 = False
        show_popup_window_p2 = False
        demo_gif.unmount()
        for component in close_button_c:
            component.unmount()
        bg_overlay.unmount()



def customization():
    global player_skins, show_popup_window
    player_skins = globals.skins

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

    preview_button_p1_c = paint_api.mount_button(  #region parameters
        px_x=globals.CENTER_X + 225,
        px_y=globals.CENTER_Y - 230,
        px_w=150,
        px_h=50,
        text="Preview",
        font_size=30,

        key="skin_preview_p1",
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

    preview_button_p2_c = paint_api.mount_button(  #region parameters
        px_x=globals.CENTER_X + 225,
        px_y=globals.CENTER_Y - 20 ,
        px_w=150,
        px_h=50,
        text="Preview",
        font_size=30,

        key="skin_preview_p2",
    )  #endregion

    back_button_c = paint_api.mount_button(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 300,
        px_w=350,
        px_h=80,
        text="Back",
        font_size=50,

        key="back",
    )  #endregion

    one_is_opened = show_popup_window_p1 or show_popup_window_p2
    if show_popup_window_p1 == 0 and show_popup_window_p2 == 0:
        if are_clicked(*preview_button_p1_c):
            show_popup_window_p1 = True
        if are_clicked(*preview_button_p2_c):
            show_popup_window_p2 = True
    if show_popup_window_p1 or show_popup_window_p2:
        pop_up_window()


    if is_clicked(left_arrow_p1, True) or is_clicked(right_arrow_p1, True):
        ind = -1 if is_clicked(left_arrow_p1) else 1
        globals.skin_p1_id = get_available_skin(globals.skin_p1_id, globals.skin_p2_id, ind)
        display_p1.set_image_path(globals.skins[f"ch{globals.skin_p1_id}"])
        save_skin_config()

    if is_clicked(left_arrow_p2, True) or is_clicked(right_arrow_p2, True):
        ind = -1 if is_clicked(left_arrow_p2) else 1
        globals.skin_p2_id = get_available_skin(globals.skin_p2_id, globals.skin_p1_id, ind)
        display_p2.set_image_path(globals.skins[f"ch{globals.skin_p2_id}"])
        save_skin_config()

    if are_clicked(*back_button_c):
        navigate("menu")
