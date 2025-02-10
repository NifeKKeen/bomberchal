from entity import Entity

class Bomb(Entity):
    timer = 0
    power = 1

    def __init__(self, x, y):
        super().__init__(x, y)
