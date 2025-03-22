import configparser
import globals
import random
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

def pop_up_window_p1():
    global show_popup_window_p1
    demo_gif = paint_api.mount_gif(
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 60,
        px_w=280,
        px_h=280,
        align="center",
        delay=1000,
        frames=[f"assets/gifs/ch{globals.skin_p1_id}/{i}.png" for i in range(1, 5)],

        key="demo_gif",
        # layer=10  # ниже, чем кнопка закрытия
    )

    close_button = paint_api.mount_rect(
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 150,
        px_w=50,
        px_h=50,
        align="center",
        image_path="assets/images/buttons/bar_button.png",
        layer=100,  # устанавливаем высокий слой для кнопки

        key="close_popup",
    )
    close_pos = close_button.px_x, close_button.px_y
    close_button_text = paint_api.mount_text(
        px_x=close_pos[0],
        px_y=close_pos[1],
        align="center",
        text="x",
        font_size=30,
        color=(255, 255, 255),
        layer=102,

        key="close_text",
    )
    close_button_shadow = paint_api.mount_text(
        px_x=close_pos[0] + globals.SHADOW_OFFSET,
        px_y=close_pos[1] + globals.SHADOW_OFFSET,
        align="center",
        text="x",
        font_size=30,
        color=globals.SHADOW_COLOR,
        layer=101,

        key="close_text_shadow",
    )
    if is_clicked(close_button):
        print("close clicked")
        show_popup_window_p1 = False
        demo_gif.unmount()
        close_button.unmount()
        close_button_shadow.unmount()
        close_button_text.unmount()

def pop_up_window_p2():
    global show_popup_window_p2
    demo_gif_p2 = paint_api.mount_gif(
        px_x=globals.center_x,
        px_y=globals.center_y,
        px_w=280,
        px_h=280,
        key="demo_gif_p2",
        delay=1000,
        frames=[f"assets/gifs/ch{globals.skin_p2_id}/{i}.png" for i in range(1, 5)],
        align="center",
    )

    close_button_p2 = paint_api.mount_rect(
        px_x=globals.center_x - 150,
        px_y=globals.center_y - 150,
        px_w=50,
        px_h=50,
        key="close_p2",  # изменён ключ
        image_path="assets/images/buttons/bar_button.png",
    )
    close_center = close_button_p2.rect.center
    close_button_text_p2 = paint_api.mount_text(
        px_x=close_center[0],
        px_y=close_center[1],
        key="close_text_p2",  # изменён ключ
        text="x",
        font_size=30,
        color=(255, 255, 255),
        layer=102,
        align="center",
    )
    close_button_shadow_p2 = paint_api.mount_text(
        px_x=close_center[0] + 4,
        px_y=close_center[1] + 4,
        key="close_text_shadow_p2",  # изменён ключ
        text="x",
        font_size=30,
        color=(0, 0, 0),
        layer=101,
        align="center",
    )
    if is_clicked(close_button_p2):
        print("close clicked")
        show_popup_window_p2 = False
        demo_gif_p2.unmount()
        close_button_p2.unmount()
        close_button_shadow_p2.unmount()
        close_button_text_p2.unmount()

def menu_customization():
    # load_config()
    # globals.player_skins = {
    #     "ch1": config.get("Skins", "player1", fallback=globals.skins["ch1"]),
    #     "ch2": config.get("Skins", "player2", fallback=globals.skins["ch2"])
    # }
    global player_skins, show_popup_window
    player_skins = globals.skins
    skin_display_index = 1

    global show_popup_window_p1
    global show_popup_window_p2
    load_config()

    paint_api.mount_text(
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 300,
        align="center",
        text="Change skin",
        font_size=40,
        color=(255, 255, 255),

        key="Customization_text",
    )
    paint_api.mount_text(
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y - 170,
        key="label_p1",
        text="for player1",
        font_size=30,
        color=(255, 255, 255),

        key="label_p0",
    )
    left_arrow_p1 = paint_api.mount_rect(
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 185,
        px_w=75,
        px_h=75,
        image_path="assets/images/buttons/left.png",

        key="left_arrow_p1",
    )
    right_arrow_p1 = paint_api.mount_rect(
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y - 185,
        px_w=75,
        px_h=75,
        image_path="assets/images/buttons/right.png",

        key="right_arrow_p1",
    )
    preview_button_p1 = paint_api.mount_rect(
        px_x=globals.CENTER_X + 225,
        px_y=globals.CENTER_Y - 230,
        px_w=150,
        px_h=50,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="skin_preview_p1",
    )
    preview_pos_p1 = preview_button_p1.px_x, preview_button_p1.px_y
    preview_button_shadow_p1 = paint_api.mount_text(
        px_x=preview_pos_p1[0] + globals.SHADOW_OFFSET,
        px_y=preview_pos_p1[1] + globals.SHADOW_OFFSET,
        align="center",
        text="Preview",
        font_size=30,
        color=globals.SHADOW_COLOR,

        key="preview_text_shadow_p1",
    )
    preview_button_text_p1 = paint_api.mount_text(
        px_x=preview_pos_p1[0],
        px_y=preview_pos_p1[1],
        align="center",
        text="Preview",
        font_size=30,
        color=(255, 255, 255),

        key="preview_text_p1",
    )
    if is_clicked(preview_button_p1):
        show_popup_window_p1 = True
    if show_popup_window_p1:
        pop_up_window_p1()

    display_p1 = paint_api.mount_rect(
        px_x=globals.CENTER_X - 40,
        px_y=globals.CENTER_Y - 230,
        px_w=160,
        px_h=160,
        # align="center",

        # image_path="assets/gifs/ch1/1.png",
        key="display_p1",
        image_path=globals.skins[f"ch{globals.skin_p1_id}"],
    )
    # image_path = globals.skins.get(f"ch{globals.skin_p1_id}")
    # if image_path is None:
    #     print("Ключ не найден в globals.skins!")
    # else:
    #     import os
    #     if os.path.exists(image_path):
    #         print("Файл найден:", image_path)
    #     else:
    #         print("Файл не найден по указанному пути:", image_path)


    if is_clicked(left_arrow_p1) or is_clicked(right_arrow_p1):
        ind = -1 if is_clicked(left_arrow_p1) else 1
        globals.skin_p1_id = (globals.skin_p1_id + ind - 1) % len(globals.skins) + 1
        display_p1.set_image_path(globals.skins[f"ch{globals.skin_p1_id}"])
        save_skin_config()

    paint_api.mount_text(
        px_x=globals.center_x - 350,
        px_y=globals.center_y + 50,
        key="label_p2_skin",
        text="for player2",
        font_size=30,
        color=(255, 255, 255),
    )
    left_arrow_p2 = paint_api.mount_rect(
        px_x=globals.center_x - 150,
        px_y=globals.center_y + 30,
        px_w=75,
        px_h=75,
        key="left_arrow_p2_skin",
        image_path="assets/images/buttons/left.png",
    )
    display_p2 = paint_api.mount_rect(
        px_x=globals.center_x - 40,
        px_y=globals.center_y + 10,
        px_w=160,
        px_h=160,
        key="display_p2",
        image_path=globals.skins[f"ch{globals.skin_p2_id}"],
    )
    right_arrow_p2 = paint_api.mount_rect(
        px_x=globals.center_x + 150,
        px_y=globals.center_y + 30,
        px_w=75,
        px_h=75,
        key="right_arrow_p2_skin",
        image_path="assets/images/buttons/right.png",
    )
    if is_clicked(left_arrow_p2) or is_clicked(right_arrow_p2):
        ind = -1 if is_clicked(left_arrow_p2) else 1
        globals.skin_p2_id = (globals.skin_p2_id + ind - 1) % len(globals.skins) + 1
        print(globals.skin_p2_id)
        display_p2.set_image_path(globals.skins[f"ch{globals.skin_p2_id}"])
        save_skin_config()

    # current_skin_p0 = player_skins["player1"]
    #     # Отображение выбранного скина
    # skin_preview = paint_api.mount_image(
    #     px_x=globals.center_x,
    #     px_y=globals.center_y,
    #     key="skin_preview",
    #     image_path=f"assets/characters/ch{skin_display_index}.png",
    #     align="center"
    preview_button_p2 = paint_api.mount_rect(
        px_x=globals.center_x + 150,
        px_y=globals.center_y - 20 ,
        px_w=150,
        px_h=50,
        key="skin_preview_p2",
        image_path="assets/images/buttons/bar_button.png",
    )
    preview_center_p2 = preview_button_p2.rect.center
    preview_button_shadow_p2 = paint_api.mount_text(
        px_x=preview_center_p2[0] + 4,
        px_y=preview_center_p2[1] + 4,
        key="preview_text_shadow_p2",
        text="Preview",
        font_size=30,
        color=(0, 0, 0),
        align="center",
    )
    preview_button_text_p2 = paint_api.mount_text(
        px_x=preview_center_p2[0],
        px_y=preview_center_p2[1],
        key="preview_text_p2",
        text="Preview",
        font_size=30,
        color=(255, 255, 255),
        align="center",
    )
    if is_clicked(preview_button_p2):
        show_popup_window_p2 = True
    if show_popup_window_p2:
        pop_up_window_p2()

    # id = 1
    # x = paint_api.mount_rect(
    #     px_y=globals.center_y + 200,
    #     px_w=80,
    #     px_h=80,
    #     key="ok",
    #     image_path= globals.skins["ch1"]
    # )

    back_button = paint_api.mount_rect(
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 300,
        px_w=350,
        px_h=80,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="back",
    )
    back_pos = back_button.px_x, back_button.px_y
    back_button_shadow = paint_api.mount_text(
        px_x=back_pos[0] + globals.SHADOW_OFFSET,
        px_y=back_pos[1] + globals.SHADOW_OFFSET,
        align="center",
        text="Back",
        font_size=50,
        color=globals.SHADOW_COLOR,

        key="back_text_shadow",
    )
    back_button_text = paint_api.mount_text(
        px_x=back_pos[0],
        px_y=back_pos[1],
        align="center",
        text="Back",
        font_size=50,
        color=(255, 255, 255),

        key="back_text",
    )

    if is_clicked(preview_button_p1):
        show_popup_window_p1 = True
    if show_popup_window_p1:
        pop_up_window_p1()
    if is_clicked(preview_button_p2):
        show_popup_window_p2 = True
    if show_popup_window_p2:
        pop_up_window_p1()

    if is_clicked(left_arrow_p1) or is_clicked(right_arrow_p1):
        ind = 1 if is_clicked(left_arrow_p1) else -1
        skin_display_index = (skin_display_index + ind) % len(globals.skins)
        # change_skin(ind, display_p0)
    if is_clicked(back_button):
        navigate("menu")
