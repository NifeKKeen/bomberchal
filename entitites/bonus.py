import globals
from entitites.bots.aggressive_bot import AggressiveBot
from entitites.bots.boss_bot import BossBot
from utils.helpers import get_tick_from_ms, rand
from entitites.entity import Entity


class Bonus(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_ENTITY_LAYER

        self.type = kwargs.get("type", globals.BONUS_SPEED)
        # Speed - multiplies speed of collector by 2 (1.25 for bosses, 1.5 for aggressive bots) for 4 seconds, but at most 8
        # Power - increases power of collector's last bomb by 2 (by 1 for aggressive bots)
        # Capacity - increases capacity (bomb_allowed) of collector by 1 for 10 seconds (does not apply for boss)
        # Life - adds extra life for collector (for boss will be added 10 lives, but with 20% chance)

        self.activated_tick = float('inf')
        self.activation_timer = kwargs.get("timer", None)

        if self.activation_timer is None:
            self.activation_timer = globals.map_bonus_type_to_timer[self.type]
        else:
            self.activation_timer = float('inf')

        self.collector = kwargs.get("collector", None)  # which entity collected bonus
        self.payload = kwargs.get("payload", None)
        self.activated = False

        self.set_image_path(globals.map_bonus_type_to_path[self.type])

    def activate(self):
        if self.activated:
            return
        self.activated = True
        self.activated_tick = self.tick

        is_boss = isinstance(self.collector, BossBot)
        is_aggressive_bot = isinstance(self.collector, AggressiveBot)

        if self.type == globals.BONUS_SPEED:
            if self.collector.speed < 8:
                self.payload = 2 if not is_aggressive_bot else 1.5 if not is_boss else 1.25

                self.collector.speed = self.collector.speed * self.payload
            else:
                self.payload = 1
        elif self.type == globals.BONUS_POWER:
            self.payload = (2 if not is_aggressive_bot else 1)

            self.collector.bomb_power += self.payload
        elif self.type == globals.BONUS_CAPACITY:
            if not is_boss:
                self.payload = 1

                self.collector.bomb_allowed += self.payload
            else:
                self.payload = 0
        elif self.type == globals.BONUS_LIFE:
            if is_boss:
                if rand(0, 100) < 20:
                    self.payload = 20
                else:
                    self.payload = 1
            else:
                self.payload = 1

            self.collector.lives += self.payload
        else:
            raise Exception("Invalid bonus type")

    def add_tick(self):
        self.tick += 1
        if not self.activated:
            return

        time_since_activated = self.tick - self.activated_tick

        if time_since_activated < self.activation_timer:  # too early
            return

        if self.type == globals.BONUS_SPEED:
            self.collector.speed /= self.payload
        elif self.type == globals.BONUS_CAPACITY:
            self.collector.bomb_allowed -= self.payload
        elif self.type == globals.BONUS_POWER:
            self.collector.bomb_power -= self.payload

        self.collector.bonuses.remove(self)
        self.kill()

def bonus_types():
    return [globals.BONUS_SPEED, globals.BONUS_POWER, globals.BONUS_CAPACITY, globals.BONUS_LIFE]

def get_bonuses(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bonus):
            res.add(entity)
    return res
