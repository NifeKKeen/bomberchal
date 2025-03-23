import globals
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.Collidable import Collidable
from utils.helpers import rand
from entitites.entity import Entity
from entitites.interfaces.Movable import Movable


class Bot(Movable, Collidable, BombSpawnable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_ENTITY_LAYER + 5

        self.bonuses = kwargs.get("bonuses", [])  # BonusItem instances
        self.moving = kwargs.get("moving",
                                 0)  # 0 if not moving (but calculating), 1 if moving by default, 2 if moves only to don't be stuck (to be entirely in the cell)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.direction = kwargs.get("direction", rand(0, 4))  # index in globals.BFS_DIRECTIONS
        self.dest_x = kwargs.get("dest_x", 0)  # destination x
        self.dest_y = kwargs.get("dest_y", 0)  # destination y
        self.dest_px_x = kwargs.get("dest_px_x", 0)  # destination px_x
        self.dest_px_y = kwargs.get("dest_px_y", 0)  # destination px_x

        self.used = [
            [False for _ in range(globals.rows)] for _ in range(globals.cols)
        ]
        self.blocked = [
            [False for _ in range(globals.rows)] for _ in range(globals.cols)
        ]
        self.dist = [
            [0 for _ in range(globals.rows)] for _ in range(globals.cols)
        ]
        self.prev = [
            [(-1, -1) for _ in range(globals.rows)] for _ in range(globals.cols)
        ]

    def add_tick(self):
        self.tick += 1
        if self.moved_this_frame:
            image_key = f"{self.last_direction}_moving"
            idx = (self.tick // 8) % len(globals.bot_frames["wandering"][image_key])
            self.set_image_path(globals.bot_frames["wandering"][image_key][idx])
        else:
            image_key = f"{self.last_direction}_static"
            idx = (self.tick // 8) % len(globals.bot_frames["wandering"][image_key])
            self.set_image_path(globals.bot_frames["wandering"][image_key][idx])

        if self.cur_damage_countdown > 0:
            self.hidden = self.cur_damage_countdown % 8 < 4
        else:
            self.hidden = False

    def think(self):
        pass


def get_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bot):
            res.add(entity)
    return res
