from entitites.bomb import Bomb
from entitites.entity import Entity
from utils.helpers import rand, get_ms_from_tick
import globals


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bomb_allowed = kwargs.get("bomb_allowed", 1)
        self.bomb_power = kwargs.get("bomb_power", 1)
        self.speed = kwargs.get("speed", 1)
        self.lives = kwargs.get("bomb_lives", 1)
        self.cooldown = kwargs.get("cooldown", 2000)
        self.bonuses = kwargs.get("bomb_bonuses", [])  # BonusItem instances

    def is_alive(self):
        return bool(self.lives)


    def spawn_bomb(self):
        # if get_ms_from_tick(self.tick) < self.cooldown:
        #     self.tick = 0
        #     return
        #print(self.x, self.y, self.px_x, self.px_y)
        self.x, self.y = self.get_pos(self.px_x, self.px_y)
        bombpx_x, bombpx_y = self.get_field_pos(self.x, self.y)
        print(self.bomb_allowed)
        if self.bomb_allowed <= 0:
            return
        print(self.x, self.y, bombpx_x, bombpx_y)

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
            timer=300,
            color=(rand(128, 256), 0, 0),
            entity_group=globals.entities,
        )
        bomb.mount()

    def add_tick(self):
        self.tick += 1

        # TEST
        if self.tick % 120 == 0:
            self.mount()

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
