from utils.helpers import rand
from entitites.entity import Entity
from entitites.interfaces.BotIntellect import BotIntellect
from entitites.interfaces.Movable import Movable


class Bot(BotIntellect, Movable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonuses = kwargs.get("bonuses", [])  # BonusItem instances

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