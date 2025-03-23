import globals
from utils.helpers import get_pos, get_tick_from_ms
from utils.paint_api import SurfaceSprite


class Entity(SurfaceSprite):
    EntityId = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_ENTITY_LAYER

        self.x = kwargs.get("x", None)  # position x in board (from left) [целые коорды]
        self.y = kwargs.get("y", None)  # position y in board (from top) [целые коорды]

        if self.x is None or self.y is None:
            self.x, self.y = get_pos(self.px_x, self.px_y)

        self.initial_lives = kwargs.get("lives", 1)
        self.lives = self.initial_lives
        self.damage_countdown = kwargs.get("damage_countdown", get_tick_from_ms(0))
        self.cur_damage_countdown = kwargs.get("cur_damage_countdown", get_tick_from_ms(0))

        self.entity_group = kwargs.get("entity_group", None)  # entity group which this entity belongs to
        if self.entity_group is not None:
            self.entity_group.add(self)

        self.entity_id = Entity.EntityId
        Entity.EntityId += 1

        self.tick = 0  # lifespan
        self.lives = kwargs.get("lives", 1)

    def is_alive(self):
        return bool(self.lives)

    def make_damage(self, damage=1):
        if self.cur_damage_countdown > 0:
            return
        self.cur_damage_countdown = self.damage_countdown
        self.lives -= damage
        if self.lives <= 0:
            self.kill()

    def kill(self):
        self.unmount()
        self.mounted = False
        if self.entity_group:
            self.entity_group.discard(self)

    def add_tick(self):
        self.tick += 1
