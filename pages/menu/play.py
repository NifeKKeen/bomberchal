import globals
from config import save_config, load_config
from pages.navigation import navigate
from utils import paint_api
from utils.interaction_api import is_clicked, are_clicked

players1_button_c = None
players2_button_c = None
pve_button_c = None
bossfight_button_c = None
duel_button_c = None
back_button_c = None


def get_setup_data_value(key):
    if globals.setup_data.__contains__(key):
        return globals.setup_data[key]
    return globals.setup_data["ranges"][globals.setup_data["index"][key]][2]


def render_range(order):
    if order < 6:
        label_pos = globals.CENTER_X + 300, 100 + order * 100
    else:
        label_pos = globals.CENTER_X - 300, 100 + (order - 6) * 100
    paint_api.mount_text(  # region parameters
        px_x=label_pos[0],
        px_y=label_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text=globals.setup_data["ranges"][order][0],
        font_size=20,
        color=(255, 255, 255),

        key=f"label_text{order}",
    )  # endregion

    item_image = None
    left_arrow = paint_api.mount_rect(  # region parameters
        px_x=label_pos[0] - 60,
        px_y=label_pos[1] + 40,
        px_w=40,
        px_h=40,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/left.png",

        key=f"left_arrow{order}",
    )  # endregion
    if globals.setup_data["ranges"][order][1]:
        item_image = paint_api.mount_rect(  # region parameters
            px_x=label_pos[0],
            px_y=label_pos[1] + 40,
            px_w=40,
            px_h=40,
            layer=globals.BUTTON_LAYER,
            align="center",
            image_path=globals.setup_data["ranges"][order][1],

            key=f"item_image{order}",
        )  # endregion
    right_arrow = paint_api.mount_rect(  # region parameters
        px_x=label_pos[0] + 60,
        px_y=label_pos[1] + 40,
        px_w=40,
        px_h=40,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/right.png",

        key=f"right_arrow{order}",
    )  # endregion
    value_text = paint_api.mount_text(  # region parameters
        px_x=label_pos[0],
        px_y=label_pos[1] + 70 if item_image else label_pos[1] + 40,
        layer=globals.TEXT_LAYER,
        align="center",
        text=str(globals.setup_data["ranges"][order][2]),
        font_size=15,
        color=(255, 255, 255),

        key=f"value_text{order}",
    )  # endregion

    globals.setup_data["ranges"][order][3] = left_arrow
    globals.setup_data["ranges"][order][4] = value_text
    globals.setup_data["ranges"][order][5] = right_arrow


def render_layout():
    global players1_button_c, players2_button_c, pve_button_c, bossfight_button_c, duel_button_c, back_button_c

    for i in range(len(globals.setup_data["ranges"])):
        render_range(i)

    players1_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X - 100,
        px_y=globals.CENTER_Y - 140,
        px_w=195,
        px_h=60,
        text="1 Player",
        font_size=30,

        key="players1_button",
    )  # endregion

    players2_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X + 100,
        px_y=globals.CENTER_Y - 140,
        px_w=195,
        px_h=60,
        text="2 Players",
        font_size=30,

        key="players2_button",
    )  # endregion

    pve_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 70,
        px_w=400,
        px_h=60,
        text="PvE",
        font_size=40,

        key="pve_button",
    )  # endregion

    bossfight_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y,
        px_w=400,
        px_h=60,
        text="Boss Fight",
        font_size=40,

        key="bossfight_button",
    )  # endregion

    duel_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 70,
        px_w=400,
        px_h=60,
        text="Duel",
        font_size=40,

        key="duel_button",
    )  # endregion

    back_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 300,
        px_w=350,
        px_h=80,
        text="Back",
        font_size=50,

        key="back",
    )  # endregion


def play(is_setup=False):
    global players1_button_c, players2_button_c, pve_button_c, bossfight_button_c, duel_button_c, back_button_c

    if is_setup:
        load_config()
        render_layout()

    for data in globals.setup_data["ranges"]:
        value = data[2]
        left_arrow = data[3]
        value_text = data[4]
        right_arrow = data[5]

        if is_clicked(left_arrow):
            if value - data[6] >= 0:
                value -= data[6]
            value_text.set_text(str(value))
        elif is_clicked(right_arrow):
            value += data[6]
            value_text.set_text(str(value))

        data[2] = value

    if are_clicked(*players1_button_c):
        globals.setup_data["players"] = 1

    elif are_clicked(*players2_button_c):
        globals.setup_data["players"] = 2

    elif are_clicked(*pve_button_c):
        globals.game_mode = "pve"
        save_config()
        navigate("game")

    elif are_clicked(*bossfight_button_c):
        globals.game_mode = "bossfight"
        save_config()
        navigate("game")

    elif are_clicked(*duel_button_c):
        globals.game_mode = "duel"
        save_config()
        navigate("game")

    elif are_clicked(*back_button_c):
        save_config()
        navigate("menu")
        return

    if globals.setup_data["players"] == 1:
        players1_button_c[1].set_color((255, 255, 0))
        players2_button_c[1].set_color((255, 255, 255))
    if globals.setup_data["players"] == 2:
        players1_button_c[1].set_color((255, 255, 255))
        players2_button_c[1].set_color((255, 255, 0))
