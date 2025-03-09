from entitites.entity import Entity
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.BotIntellect import BotIntellect
from entitites.interfaces.Movable import Movable
from entitites.interfaces.Collidable import Collidable
from utils.helpers import rand


class Bot(BotIntellect, BombSpawnable, Movable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lives = kwargs.get("bomb_lives", 1)
        self.bonuses = kwargs.get("bomb_bonuses", [])  # BonusItem instances

    def is_alive(self):
        return bool(self.lives)

    def add_tick(self):
        self.tick += 1
        if rand(1, 1000) <= 0: # test
            self.spawn_bomb()

def get_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bot):
            res.add(entity)
    return res