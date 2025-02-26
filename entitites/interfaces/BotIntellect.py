import globals

class BotIntellect:
    def think(self):
        from entitites.player import Player
        from entitites.bomb import Bomb
        from entitites.bot import Bot
        from entitites.fire import Fire
        from entitites.obstacle import Obstacle


        if not self.alive():
            return

        self.move_px(*tuple(x * self.speed for x in globals.directions[self.direction]))
        entity_lst = list(globals.entities)
        for entity in entity_lst:
            if entity == self:
                continue
            if entity.x != self.x or entity.y != self.y:
                continue
            # print("Smth on ", self.x, self.y, entity)
            if isinstance(entity, Player):
                entity.kill()
                #globals.entities.remove(entity)
                break
            elif isinstance(entity, Fire):
                self.kill()
                break
            elif isinstance(entity, Obstacle) or isinstance(entity, Bot) or isinstance(entity, Bomb):
                self.move_px(*tuple(x * -self.speed for x in globals.directions[self.direction]))
                self.direction ^= 1 # 0 to 1, 1 to 0, 2 to 3, 3 to 2 (W <-> S, A <-> D)
                # if random.randint(1, 100) <= 50: # Randomly change direction, intended to work if there is more than one direction to which we can go
                #     self.direction ^= 2
                break
