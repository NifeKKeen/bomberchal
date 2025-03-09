import globals
from entitites.bonus import Bonus
from entitites.entity import Entity
from utils.helpers import rand


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
        from entitites.bomb import Bomb
        from entitites.bot import Bot
        from entitites.fire import Fire
        from entitites.player import Player
        from entitites.obstacle import Obstacle
        from entitites.interfaces.Movable import Movable

        if isinstance(self, Player) or isinstance(self, Bot) or isinstance(self, Bomb):
            for entity in list(self.entity_group):
                if entity == self or not entity.collides_with(self):
                    continue
                # now entity collides and it is not ourselves

                if isinstance(entity, Obstacle):
                    if isinstance(self, Movable):
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

                    else:
                        self.adjust_from(entity)

                elif isinstance(entity, Bonus):
                    if isinstance(self, Bomb):
                        entity.kill()
                    else:
                        entity.collect(self)

        elif isinstance(self, Fire):
            for entity in list(self.entity_group):
                if entity == self or not entity.collides_with(self):
                    continue
                # now entity collides and it is not ourselves

                if isinstance(entity, Obstacle):
                    if entity.type == globals.D_OBSTACLE_CELL:
                        entity.kill()
                if isinstance(entity, Bomb):
                    entity.explode()
                if isinstance(entity, Player) or isinstance(entity, Bot):
                    entity.kill()


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

