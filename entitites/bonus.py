from entitites.entity import Entity
import globals
from utils.helpers import get_field_pos


class Bonus(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonus_id = kwargs.get("bonus_id", 0)
        self.timer = kwargs.get("timer", -1)
        self.type = kwargs.get("type", "Speed")
        # Speed - increases speed of collector by 2 times for 3 secs, but at most 8
        # Power - increases power of collector's last bomb by 10
        # Capacity - increases capacity (bomb_allowed) of collector by 1 for 10 secs
        self.collector = kwargs.get("collector", None)  # which entity collected bonus
        self.entity_group = kwargs.get("entity_group", "bonus")
        self.spawned_bomb = kwargs.get("spawned_bomb", False)
        self.prev_bombs_spawned = kwargs.get("prev_bombs_spawned", 0)
        self.activated = False

    def activate(self):
        if self.type == "Speed":
            if self.collector.speed >= 8:
                return
            self.collector.speed = min(self.collector.speed * 2, 8)
            self.timer = 3 * globals.FPS
        elif self.type == "Power":
            self.collector.bomb_power += 10
            self.spawned_bomb = False
        elif self.type == "Capacity":
            self.collector.bomb_allowed += 1
            self.timer = 10 * globals.FPS
        else:
            raise Exception("Invalid bonus type")

        self.activated = True

    def update(self):
        if not self.activated:
            return

        if self.timer > 0:
            self.timer -= 1
        elif self.timer == 0:
            if self.type == "Speed":
                self.collector.speed /= 2
            elif self.type == "Capacity":
                self.collector.bomb_allowed -= 1
            self.timer = -1

        if not self.collector is None and self.prev_bombs_spawned < self.collector.bombs_spawned:
            self.spawned_bomb = True
            print("!!", self.collector.bomb_power, self.collector.bombs_spawned)

        if self.spawned_bomb and self.type == "Power":
            self.collector.bomb_power -= 10
            self.spawned_bomb = False
            self.activated = False # actually already activated

        print("@@", self.collector.bomb_power, self.collector.bombs_spawned)

    def collect(self, collector):
        if len(collector.bonuses) >= 10: # at most 10 bonuses
            return
        from entitites.player import Player
        from entitites.bot import Bot
        self.collector = collector
        # print("Collected by ", collector)
        # self.kill()

        if isinstance(collector, Player) or isinstance(collector, Bot):
            collector.bonuses.append(self)

        self.activate()


def bonus_types():
    return ["Speed", "Power", "Capacity"]