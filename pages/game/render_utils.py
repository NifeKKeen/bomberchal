import globals

from pages.navigation import navigate
from utils import paint_api
from utils.helpers import get_field_pos, players_sum_of_scores
from utils.interaction_api import are_clicked
from utils.paint_api import mount_rect
from entitites.player import get_players
from utils.record_api import record_game
from utils.sound_api import play_button_click


def render_inventory():
    # 1, 2, ..., 0 for both players
    shift_x = 200
    shift_y = 20
    padding = 20

    # rendering bonuses in inventory
    for idx, player in enumerate(list(get_players(globals.entities))):
        for i in range(player.lives):
            paint_api.mount_rect(  # region parameters
                px_x=shift_x + i * 16,
                px_y=idx * padding + shift_y + (globals.rows + idx) * globals.CELL_SIZE + globals.CELL_SIZE // 2 - 30,
                px_w=15,
                px_h=15,
                layer=globals.TEXT_LAYER,
                image_path="assets/images/bonus/heart.png",

                dynamic=True,
                key=f"health-{i}-{idx}",
            )

        for i in range(1, 11):
            paint_api.mount_text(  # region parameters
                px_x=shift_x + (i - 0.75) * globals.CELL_SIZE + globals.CELL_SIZE // 2,
                px_y=idx * padding + shift_y + (globals.rows + idx) * globals.CELL_SIZE + globals.CELL_SIZE // 2,
                layer=globals.TEXT_LAYER,
                text=str(i % 10),
                font_size=16,
                color=(255, 255, 255),

                key=f"bonus_key-{i}-{idx}",
            )  # endregion
            paint_api.mount_text(  # region parameters
                px_x=shift_x + (i - 0.75) * globals.CELL_SIZE + globals.CELL_SIZE // 2 + 2,
                px_y=idx * padding + shift_y + (globals.rows + idx) * globals.CELL_SIZE + globals.CELL_SIZE // 2 + 2,
                layer=globals.SHADOW_LAYER,
                text=str(i % 10),
                font_size=16,
                color=globals.SHADOW_COLOR,

                key=f"bonus_key-{i}-{idx}-sh",
            )  # endregion

        x = 0
        for bonus in player.get_bonus_instances():

            if bonus.activated:
                continue

            npx_x, npx_y = get_field_pos(x, globals.rows + (player.key[-1] == '1'))
            mount_rect(  # region parameters
                px_x=shift_x + npx_x, px_y=idx * padding + shift_y + (globals.rows + idx) * globals.CELL_SIZE,
                px_w=bonus.px_w, px_h=bonus.px_h,
                layer=globals.BASE_ENTITY_LAYER,

                color=bonus.color,
                image_path=bonus.image_path,

                key=f"inv-{player.key}-{bonus.key}",
                dynamic=True,
            )  # endregion

            x += 1


def render_pause():
    bg_overlay = paint_api.mount_rect(  # region parameters
        px_x=0,
        px_y=0,
        px_w=globals.SCREEN_WIDTH,
        px_h=globals.SCREEN_HEIGHT,
        layer=globals.LAYER_SHIFT - 1,
        image_path="assets/images/backgrounds/overlay.png",

        key="pause_overlay",
        dynamic=True,
    )  # endregion

    unpause_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y,
        px_w=500,
        px_h=60,
        popup_layer=1,
        text="Continue",
        font_size=30,

        key="continue",
        dynamic=True,
    )  # endregion

    home_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 70,
        px_w=500,
        px_h=60,
        popup_layer=1,
        text="Exit",
        font_size=30,

        key="home",
        dynamic=True,
    )  # endregion

    if are_clicked(*unpause_button_c):
        globals.paused = False
        play_button_click()
    elif are_clicked(*home_button_c):
        play_button_click()
        navigate("menu")


def render_game_end(message, show_score, payload):
    score = players_sum_of_scores(globals.scores)

    bg_overlay = paint_api.mount_rect(  # region parameters
        px_x=0,
        px_y=0,
        px_w=globals.SCREEN_WIDTH,
        px_h=globals.SCREEN_HEIGHT,
        layer=globals.LAYER_SHIFT - 1,
        image_path="assets/images/backgrounds/overlay.png",

        key="bg_overlay",
        dynamic=True,
    )  # endregion
    game_over_text = paint_api.mount_text(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 100,
        layer=globals.TEXT_LAYER + globals.LAYER_SHIFT,
        align="center",
        text=message,
        font_size=50,
        color=(255, 255, 255),

        key="game_over_text",
        dynamic=True,
    )  # endregion

    if show_score:
        score_text = paint_api.mount_text(  # region parameters
            px_x=globals.CENTER_X,
            px_y=globals.CENTER_Y,
            layer=globals.TEXT_LAYER + globals.LAYER_SHIFT,
            align="center",
            text=f"Your score is {score}",
            font_size=30,
            color=(255, 255, 0),

            key="score_text",
            dynamic=True,
        )  # endregion

    restart_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 140,
        px_w=500,
        px_h=60,
        popup_layer=1,
        text="Restart",
        font_size=30,

        key="restart",
        dynamic=True,
    )  # endregion

    back_button_c = paint_api.mount_button(  # region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 210,
        px_w=500,
        px_h=60,
        popup_layer=1,
        text="Title screen",
        font_size=30,

        key="game_over_back",
        dynamic=True,
    )  # endregion

    if are_clicked(*restart_button_c):
        from pages.game.game import setup_game
        play_button_click()
        record_game(payload, globals.prefer_online)
        setup_game()
    elif are_clicked(*back_button_c):
        record_game(payload, globals.prefer_online)
        play_button_click()
        navigate("menu")
