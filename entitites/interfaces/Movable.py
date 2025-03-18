from entitites.entity import Entity
from utils.helpers import get_pos


class Movable(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vel_px_x = 0  # velocities for x px
        self.vel_px_y = 0  # velocity for y px
        self.speed = kwargs.get("speed", 1)
        self.moved_this_frame = False
        self.last_direction = "top"  # "right" | "down" | "left"

    def move_px(self, x=0, y=0):
        self.vel_px_x = x
        self.vel_px_y = y

        if x or y:
            self.moved_this_frame = True
            if self.vel_px_x > 0:
                self.last_direction = "right"
            elif self.vel_px_x < 0:
                self.last_direction = "left"
            elif self.vel_px_y < 0:
                self.last_direction = "top"
            else:
                self.last_direction = "down"
        else:
            self.moved_this_frame = False

        self.px_x += x
        self.px_y += y
        self.rect.x += x
        self.rect.y += y
        self.x, self.y = get_pos(self.px_x, self.px_y)
        # globals.frame_game_events.append(("move_px", (x, y)))  # TODO

    def set_px(self, x=0, y=0):
        self.px_x = x
        self.px_y = y
        self.rect.x = x
        self.rect.y = y
        self.x, self.y = get_pos(self.px_x, self.px_y)
