from entitites.bomb import Bomb
from entitites.entity import Entity
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.interfaces.Movable import Movable


class Player(Collidable, Controllable, BombSpawnable, Movable, Entity):
    def __init__(self, **kwargs):
        Controllable.__init__(self, **kwargs)
        Entity.__init__(self, **kwargs)

        self.bomb_allowed = kwargs.get("bomb_allowed", 1)
        self.bomb_power = kwargs.get("bomb_power", 1)
        self.speed = kwargs.get("speed", 10)
        self.lives = kwargs.get("bomb_lives", 1)
        self.bomb_timer = kwargs.get("bomb_timer", 2000)
        self.bonuses = kwargs.get("bomb_bonuses", [])  # BonusItem instances

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

def get_bombs(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bomb):
            res.add(entity)
    return res
