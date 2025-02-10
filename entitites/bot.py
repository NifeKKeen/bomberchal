from entity import Entity

class Bot(Entity):
    timer = 0
    speed = 1
    lives = 1

    def __init__(self, x, y):
        super().__init__(x, y)

    def is_alive(self):
        return bool(self.lives)
