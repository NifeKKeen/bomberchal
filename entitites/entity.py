from utils.paint_api import SurfaceSprite


class Entity(SurfaceSprite):
    EntityId = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.x = kwargs.get("x", 0)  # position x in board (from left) [целые коорды]
        self.y = kwargs.get("y", 0)  # position x in board (from top) [целые коорды]

        self.entity_group = kwargs.get("entity_group", None)  # entity group which this entity belongs to
        if self.entity_group is not None:
            self.entity_group.add(self)

        self.entity_id = Entity.EntityId
        Entity.EntityId += 1

        self.tick = 0  # lifespan


    def add_tick(self):
        self.tick += 1
