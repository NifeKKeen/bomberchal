from entitites.entity import Entity
from entitites.fire import Fire
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.interfaces.Movable import Movable
from utils.helpers import get_ms_from_tick, rand
import globals


class Bomb(Movable, Controllable, Collidable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = kwargs.get("timer", 0)  # in milliseconds
        self.power = kwargs.get("power", 1)
        self.spawner = kwargs.get("spawner", None)  # which entity spawned
        self.exploded = kwargs.get("exploded", False)

    def add_tick(self):
        self.tick += 1
        if self.mounted and get_ms_from_tick(self.tick) > self.timer:
            self.explode()

    def spread_fire(self):
        fire = Fire(
            timer=600,
            spread_timer=100,
            spawner=self,
            px_w=self.px_w,
            px_h=self.px_h,
            px_x=self.x * globals.cell_size,
            px_y=self.y * globals.cell_size,
            x=self.x,
            y=self.y,
            layer=self.layer + 1,
            color=(rand(128,256), 0, 0),
            power=self.power,
            entity_group=globals.entities,
        )
        fire.mount()
        if fire.spread_timer == 0:
            fire.spread()

    def explode(self):
        if self.exploded:
            return
        self.exploded = True

        if self.spawner:
            self.spawner.bomb_allowed += 1

        self.spread_fire()

        self.kill()

def get_bombs(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bomb):
            res.add(entity)
    return res
