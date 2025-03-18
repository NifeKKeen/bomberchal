import globals
from utils.helpers import rand, get_tick_from_ms
from entitites.entity import Entity


class Obstacle(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.type = kwargs.get("type", globals.D_OBSTACLE_CELL)
        self.damage_countdown = kwargs.get("damage_countdown", get_tick_from_ms(0))

        if self.mounted:
            if self.type == globals.D_OBSTACLE_CELL:
                self.set_image_path(globals.box_frames[rand(0, 2)])

            elif self.type == globals.U_OBSTACLE_CELL:
                self.set_image_path(globals.unbreakable_obstacle_frames[rand(0, 2)])

