from entitites.entity import Entity
from utils.helpers import rand, get_ms_from_tick
import globals


class Obstacle(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.type = kwargs.get("type", globals.D_OBSTACLE_CELL)