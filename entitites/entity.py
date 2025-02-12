from utils import paint_api
from utils.helpers import rand
from utils.paint_api import SurfaceSprite


class Entity(SurfaceSprite):
    EntityId = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.x = kwargs.get("x", 0)  # position x in board (from left) [целые коорды]
        self.y = kwargs.get("y", 0)  # position x in board (from top) [целые коорды]

        self.image.fill(self.color)

        self.entity_id = Entity.EntityId
        Entity.EntityId += 1

        self.tick = 0  # lifespan

        self.displayed = True  # is interactable and visible in screen


    def disable(self):
        self.displayed = False
        paint_api.unmount_sprite(self)


    def enable(self):
        self.displayed = True
        paint_api.mount_sprite(self)
