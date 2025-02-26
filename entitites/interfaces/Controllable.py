from utils.interaction_api import is_pressed, is_pressed_once


class Controllable:
    def __init__(self, **kwargs):
        self.move_left_key = kwargs.get("move_left_key", None)
        self.move_right_key = kwargs.get("move_right_key", None)
        self.move_up_key = kwargs.get("move_up_key", None)
        self.move_down_key = kwargs.get("move_down_key", None)
        self.attack_key = kwargs.get("attack_key", None)
        self.attack_func = kwargs.get("attack_func", None)

    def handle_event(self):
        if self.move_left_key and is_pressed(self.move_left_key):
            self.move_px(-self.speed, 0)
        if self.move_right_key and is_pressed(self.move_right_key):
            self.move_px(+self.speed, 0)
        if self.move_up_key and is_pressed(self.move_up_key):
            self.move_px(0, -self.speed)
        if self.move_down_key and is_pressed(self.move_down_key):
            self.move_px(0, +self.speed)
        if self.attack_key and is_pressed_once(self.attack_key):
            self.attack_func(self)
