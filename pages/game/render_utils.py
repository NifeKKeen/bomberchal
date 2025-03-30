import globals
from pages.navigation import navigate
from utils import paint_api
from utils.helpers import get_field_pos, players_sum_of_scores
from utils.interaction_api import is_clicked, are_clicked
from utils.paint_api import mount_rect
from entitites.player import get_players
from utils.scoreboard_api import save_data


def render_bonus_inventory():
    # 1, 2, ..., 0 for both players
    shift_x = 200

    # rendering bonuses in inventory
    for idx, player in enumerate(list(get_players(globals.entities))):
        for i in range(1, 11):
            paint_api.mount_text(  # region parameters
                px_x=shift_x + (i - 0.75) * globals.CELL_SIZE + globals.CELL_SIZE // 2,
                px_y=(globals.rows + idx) * globals.CELL_SIZE + globals.CELL_SIZE // 2,
                layer=globals.TEXT_LAYER,
                text=str(i % 10),
                font_size=16,
                color=(255, 255, 255),

                key=f"bonus_key-{i}-{idx}",
            )  # endregion
            paint_api.mount_text(  # region parameters
                px_x=shift_x + (i - 0.75) * globals.CELL_SIZE + globals.CELL_SIZE // 2 + 2,
                px_y=(globals.rows + idx) * globals.CELL_SIZE + globals.CELL_SIZE // 2 + 2,
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
                px_x=shift_x + npx_x, px_y=npx_y,
                px_w=bonus.px_w, px_h=bonus.px_h,
                layer=globals.BASE_ENTITY_LAYER,

                color=bonus.color,
                image_path=bonus.image_path,

                key=f"inv-{player.key}-{bonus.key}",
                dynamic=True,
            )  # endregion

            x += 1


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
        text="Title screen",
        font_size=30,

        key="game_over_back",
        dynamic=True,
    )  # endregion

    if are_clicked(*restart_button_c):
        from pages.game.game import setup_game

        save_data(payload)
        setup_game()
    elif are_clicked(back_button_c):
        save_data(payload)
        navigate("menu")
