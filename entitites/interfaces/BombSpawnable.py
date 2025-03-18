import globals
from pygame.locals import *
from utils.helpers import rand, get_field_pos, get_tick_from_ms
from entitites.entity import Entity


class BombSpawnable(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bomb_allowed = kwargs.get("bomb_allowed", 4)
        self.bomb_timer = kwargs.get("bomb_timer", get_tick_from_ms(3000))
        self.bomb_power = kwargs.get("bomb_power", 1)


    def spawn_bomb(self):
        from entitites.bomb import Bomb, get_bombs

        if self.bomb_allowed <= 0:
            return

        collision = True
        for bomb in get_bombs(globals.entities):
            if self.x == bomb.x and self.y == bomb.y:
                collision = False #there's already bomb in this position

        if not collision:
            return

        # print(self.x, self.y, self.px_x, self.px_y)
        bombpx_x, bombpx_y = get_field_pos(self.x, self.y)

        self.bomb_allowed -= 1
        bomb = Bomb(
            timer=self.bomb_timer,
            spawner=self,
            spread_type="bfs",

            layer=255,
            color=([rand(64, 128)] * 3),
            entity_group=globals.entities,

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
            px_w=globals.cell_size,
            px_h=globals.cell_size,
        )
