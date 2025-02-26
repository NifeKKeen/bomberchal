import globals


class Collidable:
    def check_collision(self):
        from entitites.fire import Fire
        from entitites.obstacle import Obstacle


        for entity in list(self.entity_group):
            if isinstance(entity, Fire):
                self.kill()
            if isinstance(entity, Obstacle):
                self.adjust()

    def adjust(self):
        self.px, self.py = self.x * globals.cell_size, self.y * globals.cell_size
