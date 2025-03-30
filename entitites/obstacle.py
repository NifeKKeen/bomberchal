import globals
from utils.helpers import rand, get_tick_from_ms, get_texture_type
from entitites.entity import Entity

MAP_SEED_OBSTACLE_KEY = {
    0: "border_obstacle",
    1: "box_obstacle",
    2: "bricks_obstacle",
}
OBSTACLE_KEY = "obstacle"


class Obstacle(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_OBSTACLE_LAYER
        self.entity_key = OBSTACLE_KEY

        self.type = kwargs.get("type", globals.D_OBSTACLE_CELL)
        self.texture_type = kwargs.get("texture_type", globals.OBSTACLE_CELL_BORDER1)
        self.seed = kwargs.get("seed", None)
        self.sub_seed = kwargs.get("sub_seed", None)
        self.damage_countdown = kwargs.get("damage_countdown", get_tick_from_ms(0))

        if self.seed is not None:
            self.entity_key = MAP_SEED_OBSTACLE_KEY[self.seed]

            self.initial_lives = globals.map_obstacle_seed_to_props[self.seed]["lives"]
            self.lives = self.initial_lives
            if self.sub_seed is None:
                self.sub_seed = rand(0, len(globals.map_obstacle_seed_to_props[self.seed]["stage_texture_types"]))
            self.texture_type = get_texture_type(globals.map_obstacle_seed_to_props[self.seed]["stage_texture_types"], self.sub_seed, 1)
        else:
            if self.sub_seed is None:
                self.sub_seed = rand(0, len(globals.map_obstacle_seed_to_props[self.seed]["stage_texture_types"]))

        if self.mounted:
            self.set_image_path(globals.map_obstacle_type_to_path[self.texture_type])

    def add_tick(self):
        self.try_snapshot()
        self.tick += 1

        if self.seed is not None:
            self.set_image_path(
                globals.map_obstacle_type_to_path[
                    get_texture_type(globals.map_obstacle_seed_to_props[self.seed]["stage_texture_types"], self.sub_seed, self.lives / self.initial_lives)
                ]
            )


def format_obstacle_key(seed=None, keyword=None):
    if seed is None:
        return f"{OBSTACLE_KEY}-{keyword}"
    else:
        return f"{MAP_SEED_OBSTACLE_KEY[seed]}-{keyword}"


def get_obstacle_key(key):
    for obstacle_key in MAP_SEED_OBSTACLE_KEY.values():
        if key.startswith(obstacle_key):
            return obstacle_key
    return None
