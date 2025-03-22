from typing import Protocol
from utils.interaction_api import is_pressed, is_pressed_once
from entitites.bot import get_bots
from entitites.entity import Entity

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
        self.movement_timer = 0 # maybe should be renamed. Means time in ticks during which a movement and/or attack occurs

    def handle_event(self):
        if not self.mounted:
            return

        total_move_x = 0
        total_move_y = 0

        if self.move_left_key and is_pressed(self.move_left_key):
            total_move_x -= self.speed

        if self.move_right_key and is_pressed(self.move_right_key):
            total_move_x += self.speed

        if self.move_up_key and is_pressed(self.move_up_key):
            total_move_y -= self.speed

        if self.move_down_key and is_pressed(self.move_down_key):
            total_move_y += self.speed

        self.move_px(total_move_x, total_move_y)

        changes = False
        if total_move_x != 0 or total_move_y != 0:
            changes = True

        if self.attack_key and is_pressed_once(self.attack_key):
            self.attack_func(self)
            changes = True

        if not changes:
            return
        else:
            self.movement_timer += 1

        # print(self.movement_timer)

        if self.movement_timer >= 20: # if something controllable changes for more than 20 ticks, distances recalculating
            self.movement_timer = 0

            # if any player moves, recalculate distances (=> destination)
            for entity in get_bots(list(self.entity_group)):
                entity.moving = 0