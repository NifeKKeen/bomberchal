import globals
from pygame.locals import *
from utils.helpers import rand, get_field_pos, get_tick_from_ms
from entitites.entity import Entity


class BombSpawnable(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bomb_allowed = kwargs.get("bomb_allowed", 3)
        self.bomb_timer = kwargs.get("bomb_timer", get_tick_from_ms(3000))
        self.bomb_power = kwargs.get("bomb_power", 1)
        self.bombs_spawned = kwargs.get("bombs_spawned", 0)
        self.bomb_countdown = kwargs.get("bomb_countdown", 0)
        self.cur_bomb_countdown = kwargs.get("cur_bomb_countdown", 0)
        self.spread_type = kwargs.get("spread_type", "bfs")


    def spawn_bomb(self):
        from entitites.bomb import Bomb, get_bombs

        if self.bomb_allowed <= 0 or self.cur_bomb_countdown > 0:
            return

        collision = True
        for bomb in get_bombs(globals.entities):
            if self.x == bomb.x and self.y == bomb.y:
                collision = False #there's already bomb in this position

        if not collision:
            return

        # print(self.x, self.y, self.px_x, self.px_y)
        bombpx_x, bombpx_y = get_field_pos(self.x, self.y)

        self.cur_bomb_countdown = self.bomb_countdown
        self.bombs_spawned += 1
        self.bomb_allowed -= 1
        bomb = Bomb(  #region parameters
            timer=self.bomb_timer,
            spawner=self,
            spread_type=self.spread_type,
            power=self.bomb_power,

            move_up_key=K_i,
            move_left_key=K_j,
            move_down_key=K_k,
            move_right_key=K_l,
            speed=10,

            x=self.x,
            y=self.y,
            px_x=bombpx_x,
            px_y=bombpx_y,
            px_w=globals.CELL_SIZE,
            px_h=globals.CELL_SIZE,

            color=([rand(64, 128)] * 3),
            entity_group=globals.entities,
        )  #endregion
