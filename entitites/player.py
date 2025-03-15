from entitites.entity import Entity
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.interfaces.Movable import Movable


class Player(Collidable, Controllable, BombSpawnable, Movable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lives = kwargs.get("lives", 1)
        self.bonuses = kwargs.get("bonuses", [])  # BonusItem instances

    def is_alive(self):
        return bool(self.lives)

    def add_tick(self):
        self.tick += 1

def get_players(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Player):
            res.add(entity)
    return res
