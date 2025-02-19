import globals
from utils.paint_api import SurfaceSprite


class Entity(SurfaceSprite):
    EntityId = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.x = kwargs.get("x", 0)  # position x in board (from left) [целые коорды]
        self.y = kwargs.get("y", 0)  # position y in board (from top) [целые коорды]

        self.entity_group = kwargs.get("entity_group", None)  # entity group which this entity belongs to
        if self.entity_group is not None:
            self.entity_group.add(self)

        self.entity_id = Entity.EntityId
        Entity.EntityId += 1

        self.tick = 0  # lifespan


    def add_tick(self):
        self.tick += 1

    def get_field_pos(self, x, y):
        px_x = x * globals.cell_size
        px_y = y * globals.cell_size
        #print(x, y, px_x, px_y, "GET FIELD POS")
        return px_x, px_y

    def get_pos(self, px_x, px_y):
        x = (px_x + globals.cell_size * 0.5) // globals.cell_size
        y = (px_y + globals.cell_size * 0.5) // globals.cell_size
        #print(px_x, px_y, x, y, "GET COORD POS")
        return x, y