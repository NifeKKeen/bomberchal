import random

from entitites.bomb import Bomb
from entitites.fire import Fire
from entitites.obstacle import Obstacle
from globals import directions
from pages.game import field_generator
from pages.game.game import *
from utils import paint_api
from pygame.locals import *

from pages.navigation import navigate
from entitites.bot import get_bots, Bot
from entitites.player import get_players, Player, get_bombs
from utils.helpers import rand, get_pos, get_field_pos
from utils.interaction_api import is_clicked, is_pressed, is_pressed_once
import globals
from utils.paint_api import SurfaceSprite

DEFAULT_FIELD = [
    [globals.VOID_CELL if rand(0, 100) < 50 else globals.U_OBSTACLE_CELL for j in range(20)] for i in range(20)
]

def setup_game(**kwargs):
    globals.cols = kwargs.get("cols", 21)
    globals.rows = kwargs.get("rows", 21)
    globals.field = kwargs.get("field", field_generator.generate(globals.rows, globals.cols))
    for i in range(2):
        rnd = rand(192, 256)
        player = Player(
            px_x=(1 if i == 0 else 19) * globals.cell_size, px_y=(1 if i == 0 else 19) * globals.cell_size,
            px_w=globals.cell_size, px_h=globals.cell_size,
            speed=2,
            color=(0, rnd / 2, rnd),
            bomb_power=3,
            bomb_allowed=5,
            layer=260,
            bomb_timer=3000,
            entity_group=globals.entities,
            key=f"player-{i}"
        )
        player.mount()

    render_field()

def render_field(**kwargs):
    field = globals.field
    for i in field:
        print(i)
    cols = globals.cols
    rows = globals.rows
    for x in range(cols):
        for y in range(rows):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                obstacle_sprite = Obstacle(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w = globals.cell_size, px_h = globals.cell_size,
                    x=x, y=y,
                    key = f"o-{x};{y}",
                    color=(64, 64, 64),
                    type=field[x][y],
                    entity_group=globals.entities)
                obstacle_sprite.mount()


            elif field[x][y] == globals.D_OBSTACLE_CELL:
                obstacle_sprite = Obstacle(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w = globals.cell_size, px_h = globals.cell_size,
                    x=x, y=y,
                    key = f"o-{x};{y}",
                    color=(255, 255, 64),
                    type=field[x][y],
                    entity_group=globals.entities)
                obstacle_sprite.mount()


            elif field[x][y] == globals.BOT_CELL:
                bot = Bot(
                    px_x=x * globals.cell_size, px_y=y * globals.cell_size,
                    px_w=globals.cell_size, px_h=globals.cell_size,
                    x=x, y=y,
                    speed=2,
                    color=(13*x, 13*y, 92 * ((x + y) % 2)),
                    layer=250,
                    entity_group=globals.entities,
                    key=f"bot-{x};{y}",
                )
                bot.mount()

def reset_game():
    globals.entities.clear()

def player_movement(player_sprites):
    players_params = []
    if len(player_sprites) >= 1:
        players_params.append([player_sprites[0], K_w, K_s, K_a, K_d, K_SPACE])
    if len(player_sprites) >= 2:
        players_params.append([player_sprites[1], K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN])

    for player in players_params:
        if player[0].alive():
            entity_lst = list(globals.entities)
            for i in range(1, 5):
                if is_pressed(player[i]):
                    player[0].move_px(*tuple(x * player[0].speed for x in globals.directions[i - 1]))
                    player[0].x, player[0].y = get_pos(player[0].px_x, player[0].px_y)
                    for entity in entity_lst:
                        if entity.x != player[0].x or entity.y != player[0].y:
                            continue
                        if isinstance(entity, Bot):
                            player[0].kill()
                            # globals.entities.remove(entity)
                            break
                        elif isinstance(entity, Obstacle):
                            player[0].move_px(*tuple(x * -player[0].speed for x in globals.directions[i - 1]))
                            break

            if is_pressed_once(player[5]):
                player[0].spawn_bomb()

def bot_movement(bot_sprites):
    for bot in bot_sprites:
        # if is_clicked(bot):
        #     bot.unmount()

        if bot.alive():
            bot.move_px(*tuple(x * bot.speed for x in globals.directions[bot.direction]))
            bot.x, bot.y = get_pos(bot.px_x, bot.px_y)
            # print(tuple(x * bot.speed for x in globals.directions[bot.direction]), "MOVEMENT DLYA BOTA", bot.direction, bot)
            entity_lst = list(globals.entities)
            for entity in entity_lst:
                if entity == bot:
                    continue
                if entity.x != bot.x or entity.y != bot.y:
                    continue
                # print("Smth on ", bot.x, bot.y, entity)
                if isinstance(entity, Player):
                    entity.kill()
                    #globals.entities.remove(entity)
                    break
                elif isinstance(entity, Fire):
                    bot.kill()
                    globals.entities.remove(bot)
                    break
                elif isinstance(entity, Obstacle) or isinstance(entity, Bot):
                    bot.move_px(*tuple(x * -bot.speed for x in globals.directions[bot.direction]))
                    bot.x, bot.y = get_pos(bot.px_x, bot.px_y)
                    bot.direction ^= 1 # 0 to 1, 1 to 0, 2 to 3, 3 to 2 (W <-> S, A <-> D)
                    # if random.randint(1, 100) <= 50: # Randomly change direction, intended to work if there is more than one direction to which we can go
                    #     bot.direction ^= 2
                    break

def game(**kwargs):
    is_setup = kwargs.get("is_setup", False)
    if is_setup:
        setup_game(**kwargs)
        return

    go_menu_button_sprite = paint_api.mount_rect(px_x=0, px_y=0, px_w=40, px_h=40, layer=300, key="go_menu")

    player_sprites = []
    bot_sprites = []
    player_entities = sorted(list(get_players(globals.entities)), key=lambda e: e.entity_id )
    bot_entities = sorted(list(get_bots(globals.entities)), key=lambda e: e.entity_id )

    for player in player_entities:
        player_sprites.append(player)
    for bot in bot_entities:
        bot_sprites.append(bot)

    player_movement(player_sprites)
    bot_movement(bot_sprites)

    if is_clicked(go_menu_button_sprite):
        navigate("menu")

    # if player1_sprite.collides_with(player2_sprite):
    #     print("Che tam")
    # print(SurfaceSprite.SurfaceId)
    globals.tick += 1
    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        entity.add_tick()
        # if isinstance(entity, Fire):
            # entity.explode()
            # entity.exploded = True
