from entitites.bomb import Bomb
from entitites.entity import Entity
from utils.helpers import rand
import globals


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bomb_allowed = kwargs.get("bomb_allowed", 1)
        self.bomb_power = kwargs.get("bomb_power", 1)
        self.speed = kwargs.get("speed", 1)
        self.lives = kwargs.get("bomb_lives", 1)
        self.bonuses = kwargs.get("bomb_bonuses", [])  # BonusItem instances

    def is_alive(self):
        return bool(self.lives)

    def spawn_bomb(self):
        if self.bomb_allowed <= 0:
            return

        self.bomb_allowed -= 1

        bomb = Bomb(
            spawner=self,
            px_w=40,
            px_h=40,
            px_x=self.px_x,
            px_y=self.px_y,
            layer=255,
            timer=3000,
            color=(rand(128, 256), 0, 0),
            entity_group=globals.entities,
        )
        bomb.mount()

    def add_tick(self):
        self.tick += 1

        # TEST
        if self.tick % 120 == 0:
            self.mount()


def get_players(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Player):
            res.add(entity)
    return res
