from entitites.entity import Entity
import globals


class Obstacle(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.type = kwargs.get("type", globals.D_OBSTACLE_CELL)