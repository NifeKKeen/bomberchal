from entitites.bomb import Bomb
from entitites.bot import Bot
from entitites.fire import Fire
from entitites.obstacle import Obstacle
from globals import directions
from pages.game import field_generator
from pages.game.game import *
from utils import paint_api
from pygame.locals import *

from pages.navigation import navigate
from entitites.player import get_players, Player, get_bombs
from utils.helpers import rand
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
            bomb_power=4,
            bomb_allowed=5,
            layer=260,
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
                    key=f"bot-{x},{y}",
                )
                bot.mount()

def reset_game():
    globals.entities.clear()

def movement(player_sprites):
    players_params = []
    if len(player_sprites) >= 1:
        players_params.append([player_sprites[0], K_w, K_s, K_a, K_d, K_SPACE])
    if len(player_sprites) >= 2:
        players_params.append([player_sprites[1], K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN])

    for player in players_params:
        if is_clicked(player[0]):
            player[0].unmount()

        if player[0].alive():
            entity_lst = list(globals.entities)
            if is_pressed(player[1]):
                player[0].move_px(0, -player[0].speed)
                for entity in entity_lst:
                    if entity.x != player[0].x or entity.y != player[0].y:
                        continue
                    if isinstance(entity, Bot):
                        player[0].unmount()
                        globals.entities.remove(entity)
                        break
                    elif isinstance(entity, Obstacle):
                        player[0].move_px(0, +player[0].speed)
                        break

            if is_pressed(player[2]):
                player[0].move_px(0, +player[0].speed)
                for entity in entity_lst:
                    if entity.x != player[0].x or entity.y != player[0].y:
                        continue
                    if isinstance(entity, Bot):
                        player[0].unmount()
                        globals.entities.remove(entity)
                        break
                    elif isinstance(entity, Obstacle):
                        player[0].move_px(0, -player[0].speed)
                        break

            if is_pressed(player[3]):
                player[0].move_px(-player[0].speed, 0)
                for entity in entity_lst:
                    if entity.x != player[0].x or entity.y != player[0].y:
                        continue
                    if isinstance(entity, Bot):
                        player[0].unmount()
                        globals.entities.remove(entity)
                        break
                    elif isinstance(entity, Obstacle):
                        player[0].move_px(+player[0].speed, 0)
                        break

            if is_pressed(player[4]):
                player[0].move_px(+player[0].speed, 0)
                for entity in entity_lst:
                    if entity.x != player[0].x or entity.y != player[0].y:
                        continue
                    if isinstance(entity, Bot):
                        player[0].unmount()
                        globals.entities.remove(entity)
                        break
                    elif isinstance(entity, Obstacle):
                        player[0].move_px(-player[0].speed, 0)
                        break


            if is_pressed_once(player[5]):
                player[0].spawn_bomb()

def game(**kwargs):
    is_setup = kwargs.get("is_setup", False)
    if is_setup:
        setup_game(**kwargs)
        return

    go_menu_button_sprite = paint_api.mount_rect(px_x=0, px_y=0, px_w=40, px_h=40, layer=300, key="go_menu")

    player_sprites = []
    player_entities = sorted(list(get_players(globals.entities)), key=lambda e: e.entity_id )

    for player in player_entities:
        player_sprites.append(player)

    if is_clicked(go_menu_button_sprite):
        navigate("menu")


    movement(player_sprites)

    # if player1_sprite.collides_with(player2_sprite):
    #     print("Che tam")
    # print(SurfaceSprite.SurfaceId)
    globals.tick += 1
    for entity in list(globals.entities):  # list to avoid "Set changed size during iteration" error
        entity.add_tick()
        # if isinstance(entity, Fire):
            # entity.explode()
            # entity.exploded = True
