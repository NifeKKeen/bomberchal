from entitites.bot import Bot
from entitites.entity import Entity
import pages.game.game
from entitites.fire import Fire
from entitites.obstacle import Obstacle
from utils.helpers import get_ms_from_tick, rand
import globals
from utils.paint_api import mount_sprite


class Bomb(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = kwargs.get("timer", 0)  # in milliseconds
        self.power = kwargs.get("power", 1)
        self.spawner = kwargs.get("spawner", None)  # which entity spawned


    def add_tick(self):
        self.tick += 1
        if self.mounted and get_ms_from_tick(self.tick) > self.timer:
            self.self_destroy()

    def explode(self):
        fire = Fire(
            spawner=self,
            px_w=self.px_w,
            px_h=self.px_h,
            px_x=self.px_x,
            px_y=self.px_y,
            x=self.x,
            y=self.y,
            layer=self.layer + 1,
            color=(rand(128,256), 0, 0),
            power=self.power,
            entity_group=globals.entities,
            key=f"f-{self.x};{self.y}"
        )
        fire.mount()
        self.entity_group.add(fire)

    def self_destroy(self):
        self.unmount()

        if self.entity_group:
            self.entity_group.discard(self)

        self.explode()

        if self.spawner:
            self.spawner.bomb_allowed += 1
