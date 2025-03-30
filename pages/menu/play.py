import globals
from config import save_config, load_config
from pages.navigation import navigate
from utils import paint_api
from utils.interaction_api import is_clicked


def get_setup_data_value(key):
    if globals.setup_data.__contains__(key):
        return globals.setup_data[key]
    return globals.setup_data["ranges"][globals.setup_data["index"][key]][2]


def render_range(order):
    if order < 6:
        label_pos = globals.CENTER_X + 300, 100 + order * 100
    else:
        label_pos = globals.CENTER_X - 300, 100 + (order - 6) * 100
    label_button_text = paint_api.mount_text(  #region parameters
        px_x=label_pos[0],
        px_y=label_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text=globals.setup_data["ranges"][order][0],
        font_size=20,
        color=(255, 255, 255),

        key=f"label_text{order}",
    )  #endregion

    item_image = None
    left_arrow = paint_api.mount_rect(  #region parameters
        px_x=label_pos[0] - 60,
        px_y=label_pos[1] + 40,
        px_w=40,
        px_h=40,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/left.png",

        key=f"left_arrow{order}",
    )  #endregion
    if globals.setup_data["ranges"][order][1]:
        item_image = paint_api.mount_rect(  #region parameters
            px_x=label_pos[0],
            px_y=label_pos[1] + 40,
            px_w=40,
            px_h=40,
            layer=globals.BUTTON_LAYER,
            align="center",
            image_path=globals.setup_data["ranges"][order][1],

            key=f"item_image{order}",
        )  #endregion
    right_arrow = paint_api.mount_rect(  #region parameters
        px_x=label_pos[0] + 60,
        px_y=label_pos[1] + 40,
        px_w=40,
        px_h=40,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/right.png",

        key=f"right_arrow{order}",
    )  #endregion
    value_text = paint_api.mount_text(  #region parameters
        px_x=label_pos[0],
        px_y=label_pos[1] + 70 if item_image else label_pos[1] + 40,
        layer=globals.TEXT_LAYER,
        align="center",
        text=str(globals.setup_data["ranges"][order][2]),
        font_size=15,
        color=(255, 255, 255),

        key=f"value_text{order}",
    )  #endregion

    globals.setup_data["ranges"][order][3] = left_arrow
    globals.setup_data["ranges"][order][4] = value_text
    globals.setup_data["ranges"][order][5] = right_arrow


def render_layout():
    global players1_button, players1_pos, players1_button_text, players1_button_shadow
    global players2_button, players2_pos, players2_button_text, players2_button_shadow
    global pve_button, pve_pos, pve_button_text, pve_button_shadow
    global bossfight_button, bossfight_pos, bossfight_button_text, bossfight_button_shadow
    global duel_button, duel_pos, duel_button_text, duel_button_shadow
    global back_button, back_pos, back_button_text, back_button_shadow

    for i in range(len(globals.setup_data["ranges"])):
        render_range(i)

    players1_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 100,
        px_y=globals.CENTER_Y - 140,
        px_w=195,
        px_h=60,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="players1_button",
    )  #endregion
    players1_pos = players1_button.px_x, players1_button.px_y
    players1_button_text = paint_api.mount_text(  #region parameters
        px_x=players1_pos[0],
        px_y=players1_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="1 Player",
        font_size=30,
        color=(255, 255, 255),

        key="players1_text",
    )  #endregion
    players1_button_shadow = paint_api.mount_text(  #region parameters
        px_x=players1_pos[0] + globals.SHADOW_OFFSET,
        px_y=players1_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text=players1_button_text.text,
        font_size=players1_button_text.font_size,
        color=globals.SHADOW_COLOR,

        key="players1_text_shadow",
    )  #endregion

    players2_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 100,
        px_y=globals.CENTER_Y - 140,
        px_w=195,
        px_h=60,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="players2_button",
    )  #endregion
    players2_pos = players2_button.px_x, players2_button.px_y
    players2_button_text = paint_api.mount_text(  #region parameters
        px_x=players2_pos[0],
        px_y=players2_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="2 Players",
        font_size=30,
        color=(255, 255, 255),

        key="players2_text",
    )  #endregion
    players2_button_shadow = paint_api.mount_text(  #region parameters
        px_x=players2_pos[0] + globals.SHADOW_OFFSET,
        px_y=players2_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text=players2_button_text.text,
        font_size=players2_button_text.font_size,
        color=globals.SHADOW_COLOR,

        key="players2_text_shadow",
    )  #endregion

    pve_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 70,
        px_w=400,
        px_h=60,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="pve_button",
    )  #endregion
    pve_pos = pve_button.px_x, pve_button.px_y
    pve_button_text = paint_api.mount_text(  #region parameters
        px_x=pve_pos[0],
        px_y=pve_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="PvE",
        font_size=40,
        color=(255, 255, 255),

        key="pve_text",
    )  #endregion
    pve_button_shadow = paint_api.mount_text(  #region parameters
        px_x=pve_pos[0] + globals.SHADOW_OFFSET,
        px_y=pve_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text=pve_button_text.text,
        font_size=pve_button_text.font_size,
        color=globals.SHADOW_COLOR,

        key="pve_text_shadow",
    )  #endregion

    bossfight_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y,
        px_w=400,
        px_h=60,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="bossfight_button",
    )  #endregion
    bossfight_pos = bossfight_button.px_x, bossfight_button.px_y
    bossfight_button_text = paint_api.mount_text(  #region parameters
        px_x=bossfight_pos[0],
        px_y=bossfight_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="Boss Fight",
        font_size=40,
        color=(255, 255, 255),

        key="bossfight_text",
    )  #endregion
    bossfight_button_shadow = paint_api.mount_text(  #region parameters
        px_x=bossfight_pos[0] + globals.SHADOW_OFFSET,
        px_y=bossfight_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text=bossfight_button_text.text,
        font_size=bossfight_button_text.font_size,
        color=globals.SHADOW_COLOR,

        key="bossfight_text_shadow",
    )  #endregion

    duel_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 70,
        px_w=400,
        px_h=60,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="duel_button",
    )  #endregion
    duel_pos = duel_button.px_x, duel_button.px_y
    duel_button_text = paint_api.mount_text(  #region parameters
        px_x=duel_pos[0],
        px_y=duel_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="Duel",
        font_size=40,
        color=(255, 255, 255),

        key="duel_text",
    )  #endregion
    duel_button_shadow = paint_api.mount_text(  #region parameters
        px_x=duel_pos[0] + globals.SHADOW_OFFSET,
        px_y=duel_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text=duel_button_text.text,
        font_size=duel_button_text.font_size,
        color=globals.SHADOW_COLOR,

        key="duel_text_shadow",
    )  #endregion

    back_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 300,
        px_w=350,
        px_h=80,
        layer=globals.LAYER_SHIFT + globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="back",
    )  #endregion
    back_pos = back_button.px_x, back_button.px_y
    back_button_text = paint_api.mount_text(  #region parameters
        px_x=back_pos[0],
        px_y=back_pos[1],
        layer=globals.LAYER_SHIFT + globals.TEXT_LAYER,
        align="center",
        text="Back",
        font_size=50,
        color=(255, 255, 255),

        key="back_text",
    )  #endregion
    back_button_shadow = paint_api.mount_text(  #region parameters
        px_x=back_pos[0] + globals.SHADOW_OFFSET,
        px_y=back_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.LAYER_SHIFT + globals.SHADOW_LAYER,
        align="center",
        text=back_button_text.text,
        font_size=back_button_text.font_size,
        color=globals.SHADOW_COLOR,

        key="back_text_shadow",
    )  #endregion


def play(is_setup=False):
    global players1_button_sprite, players1_pos, players1_button_text, players1_button_shadow
    global players2_button_sprite, players2_pos, players2_button_text, players2_button_shadow
    global pve_button_sprite, pve_pos, pve_button_text, pve_button_shadow
    global bossfight_button_sprite, bossfight_pos, bossfight_button_text, bossfight_button_shadow
    global duel_button_sprite, duel_pos, duel_button_text, duel_button_shadow
    global back_button, back_pos, back_button_text, back_button_shadow

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

    if is_clicked(players1_button):
        globals.setup_data["players"] = 1

    elif is_clicked(players2_button):
        globals.setup_data["players"] = 2

    elif is_clicked(pve_button):
        globals.game_mode = "pve"
        save_config()
        navigate("game")

    elif is_clicked(bossfight_button):
        globals.game_mode = "bossfight"
        save_config()
        navigate("game")

    elif is_clicked(duel_button):
        globals.game_mode = "duel"
        save_config()
        navigate("game")

    elif is_clicked(back_button):
        save_config()
        navigate("menu")
        return

    if globals.setup_data["players"] == 1:
        players1_button_text.set_color((255, 255, 0))
        players2_button_text.set_color((255, 255, 255))
    if globals.setup_data["players"] == 2:
        players1_button_text.set_color((255, 255, 255))
        players2_button_text.set_color((255, 255, 0))
