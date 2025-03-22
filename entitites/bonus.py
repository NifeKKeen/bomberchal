import globals
from utils.helpers import get_tick_from_ms, rand
from entitites.entity import Entity


class Bonus(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonus_id = kwargs.get("bonus_id", 0)
        self.timer = kwargs.get("timer", -1)
        self.type = kwargs.get("type", "Speed")
        # Speed - multiplies speed of collector by 2 (1.25 for bosses, 1.5 for aggressive bots) for 3 secs, but at most 8
        # Power - increases power of collector's last bomb by 2 (by 1 for aggressive bots)
        # Capacity - increases capacity (bomb_allowed) of collector by 1 for 10 secs (does not apply for boss)
        # Life - adds extra life for collector (for boss will be added 10 lives, but with 20% chance)
        self.collector = kwargs.get("collector", None)  # which entity collected bonus
        self.entity_group = kwargs.get("entity_group", "bonus")
        self.spawned_bomb = kwargs.get("spawned_bomb", False)
        self.prev_bombs_spawned = kwargs.get("prev_bombs_spawned", 0)
        self.activated = False

    def activate(self):
        from entitites.bots.original_bot import Bot
        is_boss = (globals.game_mode == "bossfight" and isinstance(self, Bot))
        is_aggressive_bot = (isinstance(self, Bot) and self.type == 3)
        if self.type == "Speed":
            if self.collector.speed >= 8:
                return
            self.collector.speed = min(self.collector.speed * (2 if not is_aggressive_bot else 1.5 if not is_boss else 1.25), 8)
            self.timer = get_tick_from_ms(3000)
        elif self.type == "Power":
            self.collector.bomb_power += (2 if not is_aggressive_bot else 1)
            self.spawned_bomb = False
        elif self.type == "Capacity":
            if is_boss:
                return
            self.collector.bomb_allowed += 1
            self.timer = get_tick_from_ms(10000)
        elif self.type == "Life":
            if is_boss:
                if rand(0, 100) < 20:
                    self.collector.lives += 20
            else:
                self.collector.lives += 1
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
                self.collector.bonuses.remove(self)
            elif self.type == "Capacity":
                self.collector.bomb_allowed -= 1
                self.collector.bonuses.remove(self)
            self.timer = -1

        if not self.collector is None and self.prev_bombs_spawned < self.collector.bombs_spawned:
            self.spawned_bomb = True
            self.prev_bombs_spawned = self.collector.bombs_spawned
            # print("!!", self.collector.bomb_power, self.collector.bombs_spawned)

        if self.spawned_bomb and self.type == "Power":
            if self in self.collector.bonuses:
                self.collector.bonuses.remove(self)
            self.collector.bomb_power -= 2
            self.spawned_bomb = False
            self.activated = False # to prevent constant decrease by 10 if bomb is already spawned

        # print("@@", self.collector.bomb_power, self.collector.bombs_spawned)

    def collect(self, collector):
        if len(collector.bonuses) >= 10: # at most 10 bonuses
            return
        from entitites.player import Player
        from entitites.bots.original_bot import Bot
        self.collector = collector
        # print("Collected by ", collector)
        # self.kill()

        if isinstance(collector, Player) or isinstance(collector, Bot):
            collector.bonuses.append(self)

        self.activate()


def bonus_types():
    return ["Speed", "Power", "Capacity", "Life"]