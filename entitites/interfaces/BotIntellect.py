import globals
from entitites.interfaces.Movable import Movable


class BotIntellect(Movable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = kwargs.get("direction", (self.y % 2) * 2) # index in globals.directions

    def think(self):
        from entitites.player import Player
        from entitites.bomb import Bomb
        from entitites.bot import Bot
        from entitites.fire import Fire
        from entitites.bonus import Bonus
        from entitites.obstacle import Obstacle


        if not self.alive():
            return

        self.type = 2 # 1 if it's bot like in original game, 2 if it's smart bot

        if self.type == 1:
            self.move_px(*tuple(x * self.speed for x in globals.directions[self.direction]))

        elif self.type == 2:
            # in this algo, bot is moving into direction of the farthest cell from all bombs
            from entitites.bomb import get_bombs
            queue = []
            used = [
                [False for j in range(globals.cols)] for i in range(globals.rows)
            ]
            dist = [
                [0 for j in range(globals.cols)] for i in range(globals.rows)
            ]
            prev = [
                [(-1, -1) for j in range(globals.cols)] for i in range(globals.rows)
            ]

            bombs_lst = list(get_bombs(globals.entities))
            for bomb in bombs_lst:
                for fx in range(1, globals.rows - 1):
                    for fy in range(1, globals.cols - 1):
                        if abs(bomb.x - fx) + abs(bomb.y - fy) <= 0: #todo: use bomb power
                            used[fx][fy] = True
                            dist[fx][fy] = 0
                            prev[fx][fy] = (fx, fy)

            for entity in list(globals.entities):
                if isinstance(entity, Bomb) or isinstance(entity, Player) or isinstance(entity, Fire):
                    x, y = entity.x, entity.y

                    if x < 0 or x >= globals.rows or y < 0 or y >= globals.cols:
                        continue


            # if isinstance(entity, Player):
                    #     # print(x, y)
                    used[x][y] = True
                    dist[x][y] = 0
                    prev[x][y] = (x, y)

            for x in range(globals.rows):
                for y in range(globals.cols):
                    if used[x][y]:
                        queue.append((x, y))

            while len(queue) > 0:
                x, y = queue[0]
                queue.pop(0)
                for dx, dy in globals.directions:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= globals.rows or ny < 0 or ny >= globals.cols:
                        continue
                    if not used[nx][ny]:
                        used[nx][ny] = True
                        prev[nx][ny] = (x, y)
                        dist[nx][ny] = dist[x][y] + 1
                        queue.append((nx, ny))

            destx, desty = int(self.x), int(self.y)
            dst = -1
            # print("Initially ", destx, desty, dist[destx][desty])


            for dx, dy in globals.directions:
                nx, ny = int(self.x) + dx, int(self.y) + dy
                if nx < 0 or nx >= globals.rows or ny < 0 or ny >= globals.cols:
                    continue

                collision = False
                for entity in list(globals.entities):
                    if entity.x != nx or entity.y != ny:
                        continue
                    if isinstance(entity, Bonus) or isinstance(entity, Obstacle):
                        continue
                    collision = True
                    break

                if collision:
                    continue
                # print("Now ", destx, desty, dist[destx][desty])
                if dist[nx][ny] >= dst:
                    dst = dist[nx][ny]
                    destx, desty = nx, ny
            # print("Now ", destx, desty, dst)

            if destx - self.x == 1:
                self.direction = 3
            elif destx - self.x == -1:
                self.direction = 2
            elif desty - self.y == 1:
                self.direction = 1
            elif desty - self.y == -1:
                self.direction = 0
            else:
                # print("Locked")
                return
            self.move_px(*tuple(x * self.speed for x in globals.directions[self.direction]))

            # print(self.x, self.y, destx, desty, self.direction, globals.directions[self.direction])


        else:
            raise Exception("Unknown type of bot!")
        entity_lst = list(globals.entities)
        for entity in entity_lst:
            if entity == self:
                continue
            if entity.x != self.x or entity.y != self.y:
                continue
            # print(entity, self, entity.collides_with(self))
            if not self.collides_with(entity):
                continue
            # print("Smth on ", self.x, self.y, entity)
            if isinstance(entity, Player):
                entity.kill()
                # globals.entities.remove(entity)
                break
            elif isinstance(entity, Fire):
                self.kill()
                break
            elif isinstance(entity, Bonus):
                entity.collect(self)
                break
            elif self.type == 1 and (isinstance(entity, Obstacle) or isinstance(entity, Bot)
                  or (isinstance(entity, Bomb) and entity.spawner != self)):
                self.move_px(*tuple(x * -self.speed for x in globals.directions[self.direction]))
                self.direction ^= 1  # 0 to 1, 1 to 0, 2 to 3, 3 to 2 (W <-> S, A <-> D)
                # if random.randint(1, 100) <= 50: # Randomly change direction, intended to work if there is more than one direction to which we can go
                #     self.direction ^= 2
                break