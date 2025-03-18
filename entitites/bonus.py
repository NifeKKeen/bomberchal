import globals
from utils.helpers import get_field_pos
from entitites.entity import Entity


class Bonus(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonus_id = kwargs.get("bonus_id", 0)
        self.timer = kwargs.get("timer", 0)
        self.type = kwargs.get("type", "Speed")
        # Speed - increases speed of collector by 2 times for 300 ticks
        # Power - increases power of collector's last bomb by 1
        # Capacity - increases capacity (bomb_allowed) of collector by 1
        self.collector = kwargs.get("collector", None)  # which entity collected bonus
        self.entity_group = kwargs.get("entity_group", "bonus")

    def collect(self, collector):
        from entitites.player import Player
        from entitites.bot import Bot
        self.collector = collector
        # print("Collected by ", collector)
        # self.kill()

        if isinstance(collector, Player) or isinstance(collector, Bot):
            collector.bonuses.append(self)

    def activate(self):
        if self.type == "Speed":
            self.collector.speed *= 2
            self.timer = 300
        elif self.type == "Power":
            self.collector.power += 1
        elif self.type == "Capacity":
            self.collector.bomb_allowed += 1
        else:
            raise Exception("Invalid bonus type")


def bonus_types():
    return ["Speed", "Power", "Capacity"]