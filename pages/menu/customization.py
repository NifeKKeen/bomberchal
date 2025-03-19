import configparser
import globals
import random
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked

CONFIG_FILE = "pages/menu/config.ini"

# def load_config():
#     config = configparser.ConfigParser()
#     config.read(CONFIG_FILE)
#     if "Skins" in config:
#         globals.skins = {
#             "ch1": config.get("Skins", "ch1", fallback=globals.skins["ch1"]),
#             "ch2": config.get("Skins", "ch2", fallback=globals.skins["ch2"])
#         }

# def get_available_skins():
#     taken = set(player_skins.values())
#     return [s for s in globals.skins if s not in taken]

# def save_skins():
#     config["Skins"] = player_skins
#     with open("settings.ini", "w") as configfile:
#         config.write(configfile)

# def assign_bot_skins():
#     available = get_available_skins()
#     random.shuffle(available)
#     return available

# bot_skins = assign_bot_skins()
# current_skin_index = 0
# def change_skin(direction, display_p0):
#     global current_skin_index
#     current_skin_index = (current_skin_index + direction) % len(globals.skins)
#     display_p0.image = globals.skins[current_skin_index]
#     while SKINS[new_index] not in available_skins:
#         new_index = (new_index + direction) % len(SKINS)
#     player_skins[player] = SKINS[new_index]

show_popup_window = False


def pop_up_window():
    global show_popup_window
    # paint_api.mount_rect(
    #     px_x=globals.center_x,
    #     px_y=globals.center_y,
    #     px_w=300,
    #     px_h=300,
    #     key="pop_up",
    #     align="center"
    # )
    # Монтируем анимированную гифку (нижний слой)
    # demo_gif = paint_api.mount_animated_gif(
    #     px_x=globals.center_x,
    #     px_y=globals.center_y,
    #     px_w=280,
    #     px_h=280,
    #     key="demo_gif",
    #     image_path="assets/gifs/1.gif",
    #     align="center",
    #     # layer=10  # ниже, чем кнопка закрытия
    # )
    demo_gif = paint_api.mount_gif(
        px_x=globals.center_x,
        px_y=globals.center_y,
        px_w=280,
        px_h=280,
        key="demo_gif",
        delay=1000,
        frames=[f"assets/gifs/ch{1}/{i}.png" for i in range(1, 5)],
        align="center",
        # layer=10  # ниже, чем кнопка закрытия
    )

    close_button = paint_api.mount_rect(
        px_x=globals.center_x - 150,
        px_y=globals.center_y - 150,
        px_w=50,
        px_h=50,
        key="close",
        image_path="assets/images/buttons/bar_button.png",
        layer=100,  # устанавливаем высокий слой для кнопки
    )
    close_center = close_button.rect.center
    close_button_text = paint_api.mount_text(
        px_x=close_center[0],
        px_y=close_center[1],
        key="close_text",
        text="x",
        font_size=30,
        color=(255, 255, 255),
        layer=102,
    )
    close_button_shadow = paint_api.mount_text(
        px_x=close_center[0] + 4,
        px_y=close_center[1] + 4,
        key="close_text_shadow",
        text="x",
        font_size=30,
        color=(0, 0, 0),
        layer=101,
    )
    close_button_text.rect.center = close_center
    close_button_shadow.rect.center = (close_center[0] + 4, close_center[1] + 4)
    if is_clicked(close_button):
        print("close clicked")
        show_popup_window = False
        demo_gif.unmount()
        close_button.unmount()
        close_button_shadow.unmount()
        close_button_text.unmount()


def menu_customization():
    # load_config()
    # globals.player_skins = {
    #     "ch1": config.get("Skins", "player1", fallback=globals.skins["ch1"]),
    #     "ch2": config.get("Skins", "player2", fallback=globals.skins["ch2"])
    # }
    global player_skins, show_popup_window
    player_skins = globals.skins
    skin_display_index = 1

    # def update_display_photo():
    # display_p0.image = f"assets/characters/ch{skin_display_index}.png"
    # paint_api.update_image("skin_preview", image_path=f"assets/characters/ch{skin_display_index}.png")

    paint_api.mount_text(
        px_x=globals.center_x,
        px_y=globals.center_y - 300,
        key="Customization_text",
        text="Change skin",
        font_size=40,
        color=(255, 255, 255),
        align="center",
    )
    paint_api.mount_text(
        px_x=globals.center_x - 350,
        px_y=globals.center_y - 170,
        key="label_p0",
        text="for player1",
        font_size=30,
        color=(255, 255, 255),
    )
    left_arrow_p0 = paint_api.mount_rect(
        px_x=globals.center_x - 150,
        px_y=globals.center_y - 185,
        px_w=75,
        px_h=75,
        key="left_arrow_p0",
        image_path="assets/images/buttons/left.png",
    )
    right_arrow_p0 = paint_api.mount_rect(
        px_x=globals.center_x + 150,
        px_y=globals.center_y - 185,
        px_w=75,
        px_h=75,
        key="right_arrow_p0",
        image_path="assets/images/buttons/right.png",
    )
    preview_button_p0 = paint_api.mount_rect(
        px_x=globals.center_x + 150,
        px_y=globals.center_y - 230,
        px_w=150,
        px_h=50,
        key="skin_preview",
        image_path="assets/images/buttons/bar_button.png",
    )
    preview_center = preview_button_p0.rect.center
    preview_button_shadow = paint_api.mount_text(
        px_x=preview_center[0] + 4,
        px_y=preview_center[1] + 4,
        key="preview_text_shadow",
        text="Preview",
        font_size=30,
        color=(0, 0, 0),
        align="center",
    )
    preview_button_text = paint_api.mount_text(
        px_x=preview_center[0],
        px_y=preview_center[1],
        key="preview_text",
        text="Preview",
        font_size=30,
        color=(255, 255, 255),
        align="center",
    )
    if is_clicked(preview_button_p0):
        show_popup_window = True
    if show_popup_window:
        pop_up_window()

    display_p0 = paint_api.mount_rect(
        px_x=globals.center_x - 40,
        px_y=globals.center_y - 230,
        px_w=160,
        px_h=160,
        key="display_p0",
        # image_path="assets/gifs/ch1/1.png",
        # align="center"
    )

    # current_skin_p0 = player_skins["player1"]
    if is_clicked(left_arrow_p0) or is_clicked(right_arrow_p0):
        ind = 1 if is_clicked(left_arrow_p0) else -1
        skin_display_index = (skin_display_index + ind) % len(globals.skins)
        # change_skin(ind, display_p0)

    #     # Отображение выбранного скина
    # skin_preview = paint_api.mount_image(
    #     px_x=globals.center_x,
    #     px_y=globals.center_y,
    #     key="skin_preview",
    #     image_path=f"assets/characters/ch{skin_display_index}.png",
    #     align="center"
    # )
    back_button = paint_api.mount_rect(
        px_y=globals.center_y + 300,
        px_w=350,
        px_h=80,
        key="back",
        image_path="assets/images/buttons/bar_button.png",
        align="center",
    )
    back_center = back_button.rect.center
    back_button_shadow = paint_api.mount_text(
        px_x=back_center[0] + 4,
        px_y=back_center[1] + 4,
        key="back_text_shadow",
        text="Back",
        font_size=50,
        color=(0, 0, 0),
        align="center",
    )
    back_button_text = paint_api.mount_text(
        px_x=back_center[0],
        px_y=back_center[1],
        key="back_text",
        text="Back",
        font_size=50,
        color=(255, 255, 255),
        align="center",
    )

    if is_clicked(back_button):
        navigate("menu")
