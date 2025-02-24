from entitites.bomb import Bomb
from entitites.entity import Entity
from utils.helpers import get_pos, get_field_pos
from utils.helpers import rand
import globals


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bomb_allowed = kwargs.get("bomb_allowed", 1)
        self.bomb_power = kwargs.get("bomb_power", 1)
        self.speed = kwargs.get("speed", 1)
        self.lives = kwargs.get("bomb_lives", 1)
        self.bomb_timer = kwargs.get("bomb_timer", 2000)
        self.bonuses = kwargs.get("bomb_bonuses", [])  # BonusItem instances

    def is_alive(self):
        return bool(self.lives)

    def spawn_bomb(self):
        if self.bomb_allowed <= 0:
            return

        #print(self.x, self.y, self.px_x, self.px_y)
        self.x, self.y = get_pos(self.px_x, self.px_y)
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
            key=f"b-{self.x};{self.y}"
        )
        bomb.mount()

    def add_tick(self):
        self.tick += 1

        # TEST
        # if self.tick % 120 == 0:
        #     self.mount()

def get_players(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Player):
            res.add(entity)
    return res

def get_bombs(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bomb):
            res.add(entity)
    return res
