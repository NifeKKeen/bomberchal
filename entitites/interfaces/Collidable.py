from utils.helpers import rand
from entitites.entity import Entity


class Collidable(Entity):
    def get_collisions(self):
        res = []

        for entity in self.entity_group:
            if entity == self:
                continue
            if entity.collides_with(self):
                res.append(entity)

        return res

    def handle_collision(self):
        from entitites.interfaces.BombSpawnable import BombSpawnable
        from entitites.bomb import Bomb
        from entitites.bots.original_bot import Bot
        from entitites.fire import Fire
        from entitites.bonus import Bonus
        from entitites.player import Player
        from entitites.obstacle import Obstacle
        from entitites.interfaces.Movable import Movable

        for entity in list(self.entity_group):
            if entity == self or not entity.collides_with(self):
                if isinstance(self, Bomb) and isinstance(entity, BombSpawnable) and self.spawner == entity:
                    self.is_spawner_inside = False
                continue
            # now entity collides and it is not ourselves

            if isinstance(self, Bot):
                if isinstance(entity, Player):
                    entity.make_damage(1)
                elif isinstance(entity, Bomb) and entity.spawner == self:
                    continue

            if isinstance(self, Movable):
                if isinstance(entity, Obstacle):
                    self_c_x = self.px_x + self.px_w // 2
                    self_c_y = self.px_y + self.px_h // 2
                    ent_c_x = entity.px_x + entity.px_w // 2
                    ent_c_y = entity.px_y + entity.px_h // 2

                    c_dx = self_c_x - ent_c_x
                    c_dy = self_c_y - ent_c_y

                    if abs(c_dx) == abs(c_dy):
                        if rand(0, 2) == 0:
                            self.adjust_from_x(entity)
                        else:
                            self.adjust_from_y(entity)

                    elif abs(c_dx) < abs(c_dy):
                        self.adjust_from_y(entity)
                    else:
                        self.adjust_from_x(entity)
                elif isinstance(entity, Bomb):
                    if entity.spawner == self and entity.is_spawner_inside:
                        continue  # ignore collision because the bomb was spawned immediately in spawner's position

                    self_c_x = self.px_x + self.px_w // 2
                    self_c_y = self.px_y + self.px_h // 2
                    ent_c_x = entity.px_x + entity.px_w // 2
                    ent_c_y = entity.px_y + entity.px_h // 2

                    c_dx = self_c_x - ent_c_x
                    c_dy = self_c_y - ent_c_y

                    if abs(c_dx) == abs(c_dy):
                        if rand(0, 2) == 0:
                            self.adjust_from_x(entity)
                        else:
                            self.adjust_from_y(entity)

                    elif abs(c_dx) < abs(c_dy):
                        self.adjust_from_y(entity)
                    else:
                        self.adjust_from_x(entity)


            if isinstance(self, Player) or isinstance(self, Bot):
                if isinstance(entity, Bonus):
                    entity.collect(self)

            if isinstance(self, Fire):
                if isinstance(entity, Obstacle):
                    self.self_destroy()
                    entity.make_damage(1)
                elif isinstance(entity, Bomb):
                    self.self_destroy()
                    entity.explode()
                elif isinstance(entity, Player) or isinstance(entity, Bot):
                    entity.make_damage(1)

    def adjust_from(self, entity):
        self.adjust_from_x(entity)
        self.adjust_from_y(entity)

    def adjust_from_x(self, entity):
        ent_px_w = entity.px_w
        ent_px_start_x = entity.px_x
        ent_px_end_x = entity.px_x + ent_px_w
        if self.px_x + (self.px_w // 2) < ent_px_start_x + (ent_px_w // 2):
            # print("ADJUSTED TO LEFT")
            self.set_px(ent_px_start_x - self.px_w, self.px_y)  # set lefter entity
        else:
            # print("ADJUSTED TO RIGHT")
            self.set_px(ent_px_end_x, self.px_y)  # set righter entity

    def adjust_from_y(self, entity):
        ent_px_h = entity.px_h
        ent_px_start_y = entity.px_y
        ent_px_end_y = entity.px_y + ent_px_h
        if self.px_y + (self.px_h // 2) < ent_px_start_y + (ent_px_h // 2):
            # print("ADJUSTED TO ABOVE")
            self.set_px(self.px_x, ent_px_start_y - self.px_h)  # set above entity
        else:
            # print("ADJUSTED TO BELOW")
            self.set_px(self.px_x, ent_px_end_y)  # set below entity
