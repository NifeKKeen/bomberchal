from entitites.entity import Entity

class Bot(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bomb_allowed = kwargs.get("bomb_allowed", 1)
        self.bomb_power = kwargs.get("bomb_power", 1)
        self.speed = kwargs.get("speed", 1)
        self.lives = kwargs.get("bomb_lives", 1)
        self.bonuses = kwargs.get("bomb_bonuses", [])  # BonusItem instances

    def is_alive(self):
        return bool(self.lives)
