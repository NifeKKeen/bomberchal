import globals
from entitites.bots.aggressive_bot import AggressiveBot
from entitites.bots.boss_bot import BossBot
from utils.helpers import get_tick_from_ms, rand
from entitites.entity import Entity


class Bonus(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_ENTITY_LAYER

        self.bonus_id = kwargs.get("bonus_id", 0)
        self.timer = kwargs.get("timer", -1)
        self.type = kwargs.get("type", "Speed")
        # Speed - multiplies speed of collector by 2 (1.25 for bosses, 1.5 for aggressive bots) for 4 seconds, but at most 8
        # Power - increases power of collector's last bomb by 2 (by 1 for aggressive bots)
        # Capacity - increases capacity (bomb_allowed) of collector by 1 for 10 seconds (does not apply for boss)
        # Life - adds extra life for collector (for boss will be added 10 lives, but with 20% chance)
        self.collector = kwargs.get("collector", None)  # which entity collected bonus
        self.modifier = kwargs.get("modifier", 0)
        self.entity_group = kwargs.get("entity_group", "bonus")
        self.spawned_bomb = kwargs.get("spawned_bomb", False)
        self.prev_bombs_spawned = kwargs.get("prev_bombs_spawned", 0)
        self.activated = kwargs.get("activated", False)

    def activate(self):
        is_boss = isinstance(self.collector, BossBot)
        is_aggressive_bot = isinstance(self.collector, AggressiveBot)
        if self.type == "Speed":
            if self.collector.speed < 8:
                self.modifier = 2 if not is_aggressive_bot else 1.5 if not is_boss else 1.25
                self.collector.speed = min(self.collector.speed * self.modifier, 8)
                self.timer = get_tick_from_ms(4000)
        elif self.type == "Power":
            self.modifier = (2 if not is_aggressive_bot else 1)
            self.collector.bomb_power += self.modifier
            self.spawned_bomb = False
        elif self.type == "Capacity":
            if not is_boss:
                self.modifier = 1
                self.collector.bomb_allowed += self.modifier
                self.timer = get_tick_from_ms(10000)
        elif self.type == "Life":
            if is_boss:
                if rand(0, 100) < 20:
                    self.modifier = 20
            else:
                self.modifier = 1
            self.collector.lives += self.modifier
        else:
            raise Exception("Invalid bonus type")

        self.activated = True
        self.unmount()

    def update(self):
        if not self.activated:
            return

        if self.timer > 0:
            self.timer -= 1
        elif self.timer == 0:
            if self.type == "Speed":
                self.collector.speed /= self.modifier
                self.collector.bonuses.remove(self)
            elif self.type == "Capacity":
                self.collector.bomb_allowed -= self.modifier
                self.collector.bonuses.remove(self)
            self.timer = -1

        if not self.collector is None and self.prev_bombs_spawned < self.collector.bombs_spawned:
            self.spawned_bomb = True
            self.prev_bombs_spawned = self.collector.bombs_spawned

        if self.spawned_bomb and self.type == "Power":
            if self in self.collector.bonuses:
                self.collector.bonuses.remove(self)
            self.collector.bomb_power -= self.modifier
            self.spawned_bomb = False
            self.activated = False # to prevent constant decrease by 2 if bomb is already spawned

    def collect(self, collector):
        from entitites.player import Player
        from entitites.bots.original_bot import Bot
        x = 0
        for bonus in collector.bonuses:
            if not bonus.mounted:
                continue
            x += 1
        if x >= 10: # at most 10 bonuses
            return

        self.collector = collector
        # print("Collected by ", collector)

        if isinstance(collector, Player) or isinstance(collector, Bot):
            collector.bonuses.append(self)
            if isinstance(collector, Bot):
                self.activate()

def bonus_types():
    return ["Speed", "Power", "Capacity", "Life"]

def get_bonuses(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bonus):
            res.add(entity)
    return res
