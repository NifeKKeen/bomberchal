from utils.helpers import get_pos
from utils.paint_api import SurfaceSprite

class Entity(SurfaceSprite):
    EntityId = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.x = kwargs.get("x", None)  # position x in board (from left) [целые коорды]
        self.y = kwargs.get("y", None)  # position y in board (from top) [целые коорды]

        if self.x is None or self.y is None:
            self.x, self.y = get_pos(self.px_x, self.px_y)

        self.entity_group = kwargs.get("entity_group", None)  # entity group which this entity belongs to
        if self.entity_group is not None:
            self.entity_group.add(self)

        self.entity_id = Entity.EntityId
        Entity.EntityId += 1

        self.mounted = False
        if kwargs.get("key") is None:
            self.key = f"e-{self.entity_id}"

        self.tick = 0  # lifespan

    def kill(self):
        self.unmount()
        self.mounted = False
        if self.entity_group:
            self.entity_group.discard(self)

    def add_tick(self):
        self.tick += 1
