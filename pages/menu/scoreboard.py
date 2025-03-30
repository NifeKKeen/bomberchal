import pygame
import globals
from utils import paint_api  # изменено для использования scoreboard_api3
from pages.navigation import navigate
from utils.interaction_api import is_clicked
from utils import scoreboard_api as scoreboard_api

game_mode = "pve"
pve_sprite = None
duel_sprite = None
bossfight_sprite = None
pve_text = None
duel_text = None
bossfight_text = None
back_button = None
back_button_text = None
header_text = "Scoreboard"

def table():
    font_size = 30
    padding = int(font_size * 0.8)
    y_offset = globals.CENTER_Y - 100
    if game_mode == "duel":
        header_text = f"{'Username':<12} {'Wins':^6} {'Losses':^6} {'Draws':^6}"
    else:
        header_text = f"{'Username':<12} {'Score':^10}"
    paint_api.mount_text(
        px_x=globals.CENTER_X,
        px_y=y_offset,
        align="center",
        text=header_text,
        font_size=font_size,
        color=(255, 255, 255),
        key="scoreboard_header",
    )
    y_offset += font_size + padding

    # Отрисовка строк с результатами
    score_data = scoreboard_api.get_scoreboard(game_mode)
    for i, entry in enumerate(score_data):
        if game_mode in ("pve", "bossfight"):
            key_mode = "pve" if game_mode == "pve" else "bossfight"
            line_text = f"{entry.get('username', ''):<12} {entry.get(key_mode, {}).get('score', 0):^10}"
        elif game_mode == "duel":
            duel = entry.get("duel", {"wins": 0, "losses": 0, "draws": 0})
            line_text = f"{entry.get('username', ''):<12} {duel.get('wins', 0):^6} {duel.get('losses', 0):^6} {duel.get('draws', 0):^6}"
        paint_api.mount_text(
            px_x=globals.CENTER_X,
            px_y=y_offset,
            align="center",
            text=line_text,
            font_size=font_size,
            color=(255, 255, 255),
            key=f"scoreboard_line_{i}",
        )
        y_offset += font_size + padding

def mount_sprites():
    global game_mode, pve_sprite, duel_sprite, bossfight_sprite
    global pve_text, duel_text, bossfight_text
    global back_button, back_button_text
    global header_text, y_offset, font_size
    y_offset = globals.CENTER_Y - 300

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

def menu_scoreboard():
    global game_mode, pve_sprite, duel_sprite, bossfight_sprite
    global pve_text, duel_text, bossfight_text
    global back_button, back_button_text, header_text
    global y_offset, font_size

    # Если спрайты ещё не смонтированы, монтируем их
    if pve_sprite is None or duel_sprite is None or bossfight_sprite is None or back_button is None:
        mount_sprites()

    # Очистка предыдущих элементов
    for key in ["scoreboard_header"] + [f"scoreboard_line_{i}" for i in range(5)]:
        if key in globals.map_key_sprite:
            paint_api.unmount(key)

    # Отрисовка таблицы
    table()
    
    # Обработка кликов по режимам (с проверками на None)
    if pve_sprite is not None and is_clicked(pve_sprite):
        game_mode = "pve"
    elif duel_sprite is not None and is_clicked(duel_sprite):
        game_mode = "duel"
    elif bossfight_sprite is not None and is_clicked(bossfight_sprite):
        game_mode = "bossfight"

    # Обновление цвета текста выбранного режима
    if game_mode == "pve":
        pve_text.set_color((255, 255, 0))
        duel_text.set_color((255, 255, 255))
        bossfight_text.set_color((255, 255, 255))
    elif game_mode == "duel":
        pve_text.set_color((255, 255, 255))
        duel_text.set_color((255, 255, 0))
        bossfight_text.set_color((255, 255, 255))
    elif game_mode == "bossfight":
        pve_text.set_color((255, 255, 255))
        duel_text.set_color((255, 255, 255))
        bossfight_text.set_color((255, 255, 0))
      
    # Обработка клика по кнопке "Back"
    if back_button is not None and is_clicked(back_button):
        navigate("menu")