import globals
from entitites.interfaces.Snapshotable import Snapshotable
from utils import snapshot_api
from utils.helpers import get_pos, get_tick_from_ms
from utils.paint_api import SurfaceSprite


ENTITY_KEY = "entity"


class Entity(SurfaceSprite, Snapshotable):
    EntityId = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_ENTITY_LAYER
        self.entity_key = ENTITY_KEY
        self._removed = False  # removed from memory
        snapshot_api.spawn_happened(self)

        self.x = kwargs.get("x", None)  # position x in board (from left) [целые коорды]
        self.y = kwargs.get("y", None)  # position y in board (from top) [целые коорды]

        if self.x is None or self.y is None:
            self.x, self.y = get_pos(self.px_x, self.px_y)

        self.initial_lives = kwargs.get("lives", 1)
        self.lives = self.initial_lives
        self.damage_countdown = kwargs.get("damage_countdown", get_tick_from_ms(0))
        self.cur_damage_countdown = kwargs.get("cur_damage_countdown", get_tick_from_ms(0))
        self.damaged_by = {}
        self.killer_key = None

        globals.entities.add(self)
        self.entity_id = Entity.EntityId
        Entity.EntityId += 1

        self.tick = 0  # lifespan

    def is_alive(self):
        return bool(self.lives)

    def make_damage(self, damage=1, damager_key=None):
        if self.cur_damage_countdown > 0:
            return
        self.cur_damage_countdown = self.damage_countdown

        true_damage = min(damage, self.lives)
        self.lives -= true_damage

        if damager_key is not None:
            from entitites.player import PLAYER_KEY

            self.damaged_by.setdefault(damager_key, 0)
            self.damaged_by[damager_key] += true_damage

            if is_entity_key(PLAYER_KEY, damager_key):
                globals.scores.setdefault(damager_key, 0)
                if damager_key == self.key:
                    add_score(damager_key, globals.scoring["SELF_DAMAGE"])
                elif globals.scoring["DAMAGE"].__contains__(self.entity_key):
                    add_score(damager_key, globals.scoring["DAMAGE"][self.entity_key])

        if self.lives <= 0:
            self.kill(killer_key=damager_key)

    def kill(self, remove_from_memory=False, killer_key=None):
        if killer_key is not None:
            from entitites.player import PLAYER_KEY

            self.killer_key = killer_key

            for damager_key, damage in self.damaged_by.items():
                if is_entity_key(PLAYER_KEY, damager_key):
                    ratio = damage / self.initial_lives
                    if damager_key != self.key:
                        if globals.scoring["KILL"].__contains__(self.entity_key):
                            # we have scoring to this entity type when killed
                            add_score(damager_key, int(globals.scoring["KILL"][self.entity_key] * ratio))
                    else:
                        add_score(damager_key, int(globals.scoring["SELF_KILL"] * ratio))


        self.unmount()
        globals.entities.discard(self)

        if remove_from_memory:
            self._kill_from_memory()
        else:
            snapshot_api.kill_happened(self)

    def _kill_from_memory(self):
        self._removed = True
        super().kill()

    def add_tick(self):
        self.try_snapshot()
        self.tick += 1


def format_entity_key(entity_key, keyword):
    return f"{entity_key}-{keyword}"


def is_entity_key(entity_key, key):
    return key.startswith(f"{entity_key}-")


def add_score(key, score):
    globals.scores.setdefault(key, 0)
    globals.scores[key] += score
