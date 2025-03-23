import globals
from utils.helpers import rand, get_tick_from_ms, get_texture_type
from entitites.entity import Entity


class Obstacle(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_OBSTACLE_LAYER

        self.type = kwargs.get("type", globals.D_OBSTACLE_CELL)
        self.texture_type = kwargs.get("texture_type", globals.OBSTACLE_CELL_BORDER1)
        self.seed = kwargs.get("seed", None)
        self.sub_seed = kwargs.get("sub_seed", None)
        self.damage_countdown = kwargs.get("damage_countdown", get_tick_from_ms(0))

        if self.seed is not None:
            self.initial_lives = globals.map_obstacle_seed_to_props[self.seed]["lives"]
            self.lives = self.initial_lives
            if self.sub_seed is None:
                self.sub_seed = rand(0, len(globals.map_obstacle_seed_to_props[self.seed]["stage_texture_types"]))
            self.texture_type = get_texture_type(globals.map_obstacle_seed_to_props[self.seed]["stage_texture_types"], self.sub_seed, 1)
        else:
            if self.sub_seed is None:
                self.sub_seed = rand(0, len(globals.map_obstacle_seed_to_props[self.seed]["stage_texture_types"]))

        if self.mounted:
            self.set_image_path(globals.map_type_to_path[self.texture_type])

    def add_tick(self):
        self.tick += 1
        if self.seed is not None:
            self.set_image_path(
                globals.map_type_to_path[
                    get_texture_type(globals.map_obstacle_seed_to_props[self.seed]["stage_texture_types"], self.sub_seed, self.lives / self.initial_lives)
                ]
            )

