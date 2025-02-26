import globals
from utils.helpers import rand, get_field_pos


class BombSpawnable:
    def spawn_bomb(self):
        from entitites.bomb import Bomb
        from entitites.player import get_bombs

        if self.bomb_allowed <= 0:
            return

        collision = True
        for bomb in get_bombs(globals.entities):
            if self.x == bomb.x and self.y == bomb.y:
                collision = False #there's already bomb in this position

        if not collision:
            return

        #print(self.x, self.y, self.px_x, self.px_y)
        bombpx_x, bombpx_y = get_field_pos(self.x, self.y)

        self.bomb_allowed -= 1
        bomb = Bomb(
            spawner=self,
            px_w=globals.cell_size,
            px_h=globals.cell_size,
            x=self.x,
            y=self.y,
            px_x=bombpx_x,
            px_y=bombpx_y,
            layer=255,
            timer=self.bomb_timer,
            color=([rand(64, 128)] * 3),
            entity_group=globals.entities,
            power=self.bomb_power,
        )
        bomb.mount()
