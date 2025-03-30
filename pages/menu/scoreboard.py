import globals
from utils import paint_api
from utils.interaction_api import is_clicked, are_clicked
from utils import scoreboard_api as scoreboard_api
from pages.navigation import navigate


pve_button_c = None
duel_button_c = None
bossfight_button_c = None
back_button_c = None

selected_game_mode = "pve"


def render_table():
    header_text = "Scoreboard"
    font_size = 30
    padding = int(font_size * 0.8)
    initial_y_offset = globals.CENTER_Y - 100

    if selected_game_mode == "duel":
        header_text = f"{'Username':<12} {'Wins':^6} {'Losses':^6} {'Draws':^6}"
    else:
        header_text = f"{'Username':<12} {'Score':^10}"

    paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X,
        px_y=initial_y_offset,
        align="center",
        text=header_text,
        font_size=font_size,
        color=(255, 255, 255),

        dynamic=True,
        key="scoreboard_header",
    )  # endregion
    y_offset = initial_y_offset + font_size + padding

    # Rendering results
    score_data = scoreboard_api.get_scoreboard(selected_game_mode)
    for i, entry in enumerate(score_data):
        if i > 5:
            break

        if selected_game_mode in ("pve", "bossfight"):
            key_mode = "pve" if selected_game_mode == "pve" else "bossfight"
            line_text = f"{entry.get('username', ''):<12} {entry.get(key_mode, {}).get('score', 0):^10}"
        elif selected_game_mode == "duel":
            duel = entry.get("duel", {"wins": 0, "losses": 0, "draws": 0})
            line_text = f"{entry.get('username', ''):<12} {duel.get('wins', 0):^6} {duel.get('losses', 0):^6} {duel.get('draws', 0):^6}"
        paint_api.mount_text(
            px_x=globals.CENTER_X,
            px_y=y_offset,
            align="center",
            text=line_text,
            font_size=font_size,
            color=(255, 255, 255),

            dynamic=True,
            key=f"scoreboard_line_{i}",
        )
        y_offset += font_size + padding


def render_scoreboard():
    global pve_button_c, duel_button_c, bossfight_button_c, back_button_c

    paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 300,
        layer=globals.TEXT_LAYER,
        align="center",
        text="Scoreboard",
        font_size=40,
        color=(255, 255, 255),
        key="scoreboard_title",
    )  # endregion

    pve_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X - 250,
        px_y=globals.CENTER_Y - 200,
        px_w=150,
        px_h=80,
        text="PvE",
        font_size=50,

        key="pve",
    )  # endregion

    duel_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X - 70,
        px_y=globals.CENTER_Y - 200,
        px_w=150,
        px_h=80,
        font_size=50,
        text="Duel",

        key="duel",
    )  # endregion

    bossfight_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X + 190,
        px_y=globals.CENTER_Y - 200,
        px_w=300,
        px_h=80,
        text="bossfight",
        font_size=50,

        key="bossfight",
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


def scoreboard(is_setup=False):
    global selected_game_mode
    global pve_button_c, duel_button_c, bossfight_button_c, back_button_c

    if is_setup:
        render_scoreboard()

    render_table()

    if are_clicked(*pve_button_c):
        selected_game_mode = "pve"
    elif are_clicked(*duel_button_c):
        selected_game_mode = "duel"
    elif are_clicked(*bossfight_button_c):
        selected_game_mode = "bossfight"

    if selected_game_mode == "pve":
        pve_button_c[1].set_color((255, 255, 0))
        duel_button_c[1].set_color((255, 255, 255))
        bossfight_button_c[1].set_color((255, 255, 255))
    elif selected_game_mode == "duel":
        pve_button_c[1].set_color((255, 255, 255))
        duel_button_c[1].set_color((255, 255, 0))
        bossfight_button_c[1].set_color((255, 255, 255))
    elif selected_game_mode == "bossfight":
        pve_button_c[1].set_color((255, 255, 255))
        duel_button_c[1].set_color((255, 255, 255))
        bossfight_button_c[1].set_color((255, 255, 0))
      
    if are_clicked(*back_button_c):
        navigate("menu")
