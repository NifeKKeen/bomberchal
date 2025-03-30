import globals
from entitites.bot import Bot
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.Collidable import Collidable
from utils.helpers import rand, in_valid_range


class OriginalBot(Bot, BombSpawnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.texture_type = "original"
        self.set_image_path(globals.bot_frames[self.texture_type]["top_static"][0])

    def think(self):
        from entitites.bomb import Bomb
        from entitites.bonus import Bonus

        if not self.alive():
            return

        self.move_px(*tuple(x * self.speed for x in globals.BFS_DIRECTIONS[self.direction]))

        collisions = Collidable.get_collisions(self)
        for entity in collisions:
            if not isinstance(entity, Bonus) and not (isinstance(entity, Bomb) and entity.spawner_key == self.key):
                self.move_px(*tuple(-x * self.speed for x in globals.BFS_DIRECTIONS[self.direction]))
                self.direction ^= 2  # 0 to 2, 2 to 0, 1 to 3, 3 to 1 (UP <-> DOWN, LEFT <-> RIGHT)
                break

        if rand(0, 100) == 0: # to simulate randomness like in actual game
            self.direction ^= 1
            locked = True

            dx, dy = globals.BFS_DIRECTIONS[self.direction]
            nx, ny = self.x + dx, self.y + dy
            if in_valid_range(nx, ny, globals.cols, globals.rows):
                if globals.field_weight[nx][ny] < globals.inf:
                    locked = False

            self.direction ^= 2

            dx, dy = globals.BFS_DIRECTIONS[self.direction]
            nx, ny = self.x + dx, self.y + dy
            if in_valid_range(nx, ny, globals.cols, globals.rows):
                if globals.field_weight[nx][ny] == globals.inf:
                    locked = False

            self.direction ^= 2
            if locked:
                self.direction ^= 1

        if rand(0, 10000) == 0:
            self.spawn_bomb()

def get_original_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, OriginalBot):
            res.add(entity)
    return res