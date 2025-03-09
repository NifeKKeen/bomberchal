from typing import Protocol

from entitites.entity import Entity
from utils.interaction_api import is_pressed, is_pressed_once

class ControllableProtocol(Protocol):
    speed: int
    vel_px_x: int
    vel_px_y: int

class Controllable(Entity, ControllableProtocol):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # if Entity.__init__ is called, it won't be called twice!

        self.move_left_key = kwargs.get("move_left_key", None)
        self.move_right_key = kwargs.get("move_right_key", None)
        self.move_up_key = kwargs.get("move_up_key", None)
        self.move_down_key = kwargs.get("move_down_key", None)
        self.attack_key = kwargs.get("attack_key", None)
        self.attack_func = kwargs.get("attack_func", None)

    def handle_event(self):
        if not self.mounted:
            return

        moved_x = False
        moved_y = False

        if self.move_left_key and is_pressed(self.move_left_key):
            self.move_px(-self.speed, 0)
            moved_x = True

        if self.move_right_key and is_pressed(self.move_right_key):
            self.move_px(+self.speed, 0)
            moved_x = True

        if self.move_up_key and is_pressed(self.move_up_key):
            self.move_px(0, -self.speed)
            moved_y = True

        if self.move_down_key and is_pressed(self.move_down_key):
            self.move_px(0, +self.speed)
            moved_y = True

        if not moved_x:
            self.vel_px_x = 0
        if not moved_y:
            self.vel_px_y = 0

        if self.attack_key and is_pressed_once(self.attack_key):
            self.attack_func(self)
