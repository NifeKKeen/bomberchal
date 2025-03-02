import globals
from entitites.interfaces.Movable import Movable
from utils.helpers import get_field_pos


class BotIntellect(Movable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = kwargs.get("direction", (self.y % 2) * 2) # index in globals.directions
        self.moving = kwargs.get("moving", False)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.destx = kwargs.get("destx", 0) # destination
        self.desty = kwargs.get("desty", 0)

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
            # if self.moving:
            #     curx, cury = self.destx, self.desty
            #     while prev[curx][cury] != (self.x, self.y):
            #         curx, cury = prev[curx][cury]
            #     self.move_px(*tuple(x * self.speed for x in globals.directions[self.direction]))
            #     return
            # in this algo, bot is moving into direction of the farthest cell from all bombs, fires and players
            from entitites.bomb import get_bombs
            queue = []
            used = [
                [False for j in range(globals.cols)] for i in range(globals.rows)
            ]
            blocked = [
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

                    used[x][y] = True
                    dist[x][y] = 0 #(-1e18 if isinstance(entity, Obstacle) else 0)
                    prev[x][y] = (x, y)

                if isinstance(entity, Obstacle):
                    x, y = entity.x, entity.y
                    if x < 0 or x >= globals.rows or y < 0 or y >= globals.cols:
                        continue
                    blocked[x][y] = True

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
                    if blocked[nx][ny]:
                        continue
                    if not used[nx][ny]:
                        used[nx][ny] = True
                        prev[nx][ny] = (x, y)
                        dist[nx][ny] = dist[x][y] + 1
                        queue.append((nx, ny))

            dst = -1

            for x in range(globals.rows):
                for y in range(globals.cols):
                    #print("DIST", x, y, dist[x][y], blocked[x][y], used[x][y])
                    if not blocked[x][y] and used[x][y] and prev[x][y] != (-1, -1):
                        print(dist[x][y], end='\t')
                        if dist[x][y] > dst:
                            destx, desty = x, y
                            dst = dist[x][y]
                    else:
                        print("-1", end='\t')
                print()
            print("Initially ", self.x, self.y, destx, desty, prev[destx][desty], used[destx][desty], dst, dist[destx][desty])
            if dst == -1:
                return

            queue = []
            used = [
                [False for j in range(globals.cols)] for i in range(globals.rows)
            ]
            blocked = [
                [False for j in range(globals.cols)] for i in range(globals.rows)
            ]
            dist = [
                [0 for j in range(globals.cols)] for i in range(globals.rows)
            ]
            prev = [
                [(-1, -1) for j in range(globals.cols)] for i in range(globals.rows)
            ]
            queue.append((destx, desty))
            used[destx][desty] = True
            prev[destx][desty] = (destx, desty)
            while len(queue) > 0:
                x, y = queue[0]
                queue.pop(0)
                for dx, dy in globals.directions:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= globals.rows or ny < 0 or ny >= globals.cols:
                        continue
                    if blocked[nx][ny]:
                        continue
                    if not used[nx][ny]:
                        used[nx][ny] = True
                        prev[nx][ny] = (x, y)
                        dist[nx][ny] = dist[x][y] + 1
                        queue.append((nx, ny))

            print("NEW DISTSTUISTHUISTIST")
            for x in range(globals.rows):
                for y in range(globals.cols):
                    #print("DIST", x, y, dist[x][y], blocked[x][y], used[x][y])
                    if not blocked[x][y] and used[x][y] and prev[x][y] != (-1, -1):
                        print(dist[x][y], end='\t')
                        if dist[x][y] > dst:
                            destx, desty = x, y
                            dst = dist[x][y]
                    else:
                        print("-1", end='\t')
                print()

            print("ww ", self.x, self.y, destx, desty, dst)
            while prev[destx][desty] != (self.x, self.y):
                print(destx, desty, prev[destx][desty], dist[destx][desty], dst, self.x, self.y)
                destx, desty = prev[destx][desty]

            print("qwe ", self.x, self.y, destx, desty, dst)

            if destx - self.x == 1:
                self.direction = 3
            elif destx - self.x == -1:
                self.direction = 2
            elif desty - self.y == 1:
                self.direction = 1
            elif desty - self.y == -1:
                self.direction = 0
            else:
                print("Locked")
                return
            #if not blocked[destx][desty]:
            self.move_px(*tuple(x * self.speed for x in globals.directions[self.direction]))
            self.moving = True

            # if collision:
            #     bombpx_x, bombpx_y = get_field_pos(self.x, self.y)
            #     self.move_px(bombpx_x - self.px_x, bombpx_y - self.px_y)

            #print(self.x, self.y, destx, desty, dst, self.direction, globals.directions[self.direction])


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