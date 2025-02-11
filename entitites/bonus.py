from entity import Entity

class Bonus(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonus_id = kwargs.get("bonus_id", 0)
        self.timer = kwargs.get("timer", 0)
