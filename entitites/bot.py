from entitites.entity import Entity
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.BotIntellect import BotIntellect
from entitites.interfaces.Movable import Movable
from utils.helpers import rand


class Bot(BotIntellect, BombSpawnable, Movable, Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)

        self.speed = kwargs.get("speed", 10)
        self.bomb_allowed = kwargs.get("bomb_allowed", 4)
        self.bomb_timer = kwargs.get("bomb_timer", 3000)
        self.bomb_power = kwargs.get("bomb_power", 1)
        self.lives = kwargs.get("bomb_lives", 1)
        self.bonuses = kwargs.get("bomb_bonuses", [])  # BonusItem instances
        self.direction = kwargs.get("direction", (self.y % 2) * 2) # index in globals.directions

    def is_alive(self):
        return bool(self.lives)

    def add_tick(self):
        self.tick += 1
        if rand(1, 1000) < 5:
            self.spawn_bomb()

def get_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bot):
            res.add(entity)
    return res