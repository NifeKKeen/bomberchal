from entity import Entity

class Bomb(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = 0
        self.power = 1
