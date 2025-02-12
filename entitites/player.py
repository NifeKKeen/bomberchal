from entitites.entity import Entity

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


def get_players(entities):
    res = []
    for entity in entities:
        if isinstance(entity, Player):
            res.append(entity)
    return res
