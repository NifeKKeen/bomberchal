import globals

from pygame.locals import *

from entitites.bomb import get_bombs
from entitites.fire import get_fires, Fire
from entitites.obstacle import Obstacle
from pages.menu.play import get_setup_data_value
from utils import paint_api, snapshot_api
from utils.helpers import rand, in_valid_range
from utils.interaction_api import is_clicked, is_pressed
from utils.sound_api import play_music
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.bots.original_bot import Bot
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.player import get_players
from entitites.bot import get_bots
from pages.game.dispatchers import build_field, spawn_bonus, reset_game
from pages.game.render_utils import render_bonus_inventory, render_game_end, render_pause
from pages.game import field_generator
from pages.navigation import navigate
from config import load_config


def setup_game():
    reset_game()
    load_config()

    globals.rows = get_setup_data_value("rows")
    globals.cols = get_setup_data_value("cols")
    globals.field = field_generator.generate(globals.cols, globals.rows, globals.game_mode)
    globals.field_fire_state = [[0] * globals.rows for _ in range(globals.cols)]
    globals.field_free_state = [[False] * globals.rows for _ in range(globals.cols)]
    globals.field_weight = [[0] * globals.rows for _ in range(globals.cols)]

    play_music(
        globals.MAP_GAMEMODE_MUSIC[globals.game_mode][0],
        globals.MAP_GAMEMODE_MUSIC[globals.game_mode][1],
        override=True
    )

    build_field()

    while len(globals.state_snapshots):
        globals.state_snapshots.pop().clear()
    globals.cur_state_spawned_sprites.clear()
    globals.cur_state_killed_sprites.clear()


def handle_game_end():
    if globals.game_mode == "pve" or globals.game_mode == "bossfight":
        if len(get_players(globals.entities)) == 0:
            render_game_end("You died!", True, {"game_mode": globals.game_mode, "payload": globals.scores})
            return True
        elif len(get_bots(globals.entities)) == 0:
            render_game_end("You won!", True, {"game_mode": globals.game_mode, "payload": globals.scores})
            return True
        else:
            return False
    elif globals.game_mode == "duel":
        players = list(get_players(globals.entities))
        if len(players) == 0:
            render_game_end("Draw!", False, {"game_mode": globals.game_mode, "payload": -1})
            return True
        if len(players) == 1:
            winner_player_id = players[0].player_id
            render_game_end(
                f"Player {winner_player_id} won!",
                False,
                {
                    "game_mode": globals.game_mode,
                    "payload": winner_player_id
                })
            return True
        else:
            return False
    return False


def game(**kwargs):
    is_setup = kwargs.get("is_setup", False)

    if is_setup:
        setup_game()

    go_menu_button_sprite = paint_api.mount_rect(  # region parameters
        px_x=0, px_y=0,
        px_w=40, px_h=40,
        layer=globals.BUTTON_LAYER + globals.LAYER_SHIFT,
        image_path="assets/images/buttons/menu.png",

        key="go_menu"
    )  # endregion

    render_bonus_inventory()

    is_game_over = handle_game_end()

    if is_clicked(go_menu_button_sprite):
        globals.paused = True

    if globals.paused:
        render_pause()
        return

    if is_pressed(K_t):
        globals.time_reversing_count_down = 2

    if globals.time_reversing_count_down:
        if globals.tick % globals.SNAPSHOT_CAPTURE_DELAY == 0:
            snapshot_api.restore_last_snapshot()
    else:
        if not is_game_over and globals.tick % globals.SNAPSHOT_CAPTURE_DELAY == 0:
            snapshot_api.capture()

    globals.time_reversing_count_down = max(0, globals.time_reversing_count_down - 1)
    if globals.time_reversing_count_down:
        return

    if is_game_over:
        return

    globals.time_slowdown_count_down = max(0, globals.time_slowdown_count_down - 1)
    if globals.time_slowdown_count_down % 4 >= 1:
        return

    globals.game_tick += 1

    for x in range(globals.cols):
        for y in range(globals.rows):
            globals.field_free_state[x][y] = False
            globals.field_weight[x][y] = 0

    for entity in list(globals.entities):
        if not in_valid_range(entity.x, entity.y, globals.cols, globals.rows):
            continue
        globals.field_free_state[entity.x][entity.y] = True

    bombs_list = list(get_bombs(globals.entities)) + list(get_fires(globals.entities))
    for bomb in bombs_list:
        for fx in range(max(1, bomb.x - bomb.power), min(globals.cols - 1, bomb.x + bomb.power + 1)):
            for fy in range(max(1, bomb.y - bomb.power), min(globals.rows - 1, bomb.y + bomb.power + 1)):
                if abs(bomb.x - fx) + abs(bomb.y - fy) <= bomb.power:
                    globals.field_weight[fx][fy] += bomb.power - (abs(bomb.x - fx) + abs(bomb.y - fy)) + 1

    for entity in list(globals.entities):
        if isinstance(entity, Fire):
            x, y = int(entity.x), int(entity.y)
            if not in_valid_range(x, y, globals.cols, globals.rows):
                continue
            globals.field_weight[x][y] += 10

        if isinstance(entity, Obstacle) or isinstance(entity, Bot):
            x, y = int(entity.x), int(entity.y)
            if not in_valid_range(x, y, globals.cols, globals.rows):
                continue
            globals.field_weight[x][y] = globals.inf

    bonus_delay = get_setup_data_value("bonus_delay")
    if bonus_delay == 0 or globals.game_tick % bonus_delay == 0:
        spawn_bonus(rand(4, 6))

    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        entity.add_tick()

        entity.cur_damage_countdown = max(entity.cur_damage_countdown - 1, 0)

        if isinstance(entity, BombSpawnable):
            entity.cur_bomb_countdown = max(entity.cur_bomb_countdown - 1, 0)
        if isinstance(entity, Controllable):
            entity.handle_event()
        if isinstance(entity, Bot):
            entity.think()

    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        if isinstance(entity, Collidable):
            entity.handle_collision()
