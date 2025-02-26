from entitites.entity import Entity
from utils.helpers import get_ms_from_tick


class Bomb(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = kwargs.get("timer", 0)  # in milliseconds
        self.power = kwargs.get("power", 1)
        self.spawner = kwargs.get("spawner", None)  # which entity spawned


    def add_tick(self):
        self.tick += 1
        if self.mounted and get_ms_from_tick(self.tick) > self.timer:
            self.self_destroy()

    def self_destroy(self):
        self.unmount()

        if self.entity_group:
            self.entity_group.discard(self)
        if self.spawner:
            self.spawner.bomb_allowed += 1
