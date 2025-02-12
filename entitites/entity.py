import pygame

from paint_api import SurfaceSprite


class Entity(SurfaceSprite):
    EntityId = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.entity_id = Entity.EntityId
        Entity.EntityId += 1

        self.tick = 0  # lifespan

        self.displayed = False  # is interactable and visible in screen


    def move_px(self, x = 0, y = 0):
        self.rect.x += x
        self.px_x += x

        self.rect.y += y
        self.px_y += y


    def disable(self):
        self.displayed = False


    def enable(self):
        self.displayed = True
