from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.Collidable import Collidable
from utils.helpers import rand, get_pos, get_field_pos, in_valid_range
from entitites.entity import Entity
from entitites.interfaces.Movable import Movable
import globals


class Bot(Movable, Collidable, BombSpawnable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonuses = kwargs.get("bonuses", [])  # BonusItem instances
        self.moving = kwargs.get("moving",
                                 0)  # 0 if not moving (but calculating), 1 if moving by default, 2 if moves only to don't be stuck (to be entirely in the cell)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.direction = kwargs.get("direction", rand(0, 4))  # index in globals.BFS_DIRECTIONS
        self.dest_x = kwargs.get("dest_x", 0)  # destination x
        self.dest_y = kwargs.get("dest_y", 0)  # destination y
        self.dest_px_x = kwargs.get("dest_px_x", 0)  # destination px_x
        self.dest_px_y = kwargs.get("dest_px_y", 0)  # destination px_x
        self.type = kwargs.get("type", 2)
        # 1 if it's bot like in original game, 2 if it's wandering bot, 3 if it's aggressive bot

        self.used = [
            [False for j in range(globals.rows)] for i in range(globals.cols)
        ]
        self.blocked = [
            [False for j in range(globals.rows)] for i in range(globals.cols)
        ]
        self.dist = [
            [0 for j in range(globals.rows)] for i in range(globals.cols)
        ]
        self.prev = [
            [(-1, -1) for j in range(globals.rows)] for i in range(globals.cols)
        ]

    def add_tick(self):
        self.tick += 1
        if rand(1, 1000) <= 0: # test
            self.spawn_bomb()

    def think(self):
        from entitites.player import Player, get_players
        from entitites.bomb import Bomb
        from entitites.bomb import get_bombs
        from entitites.bot import Bot
        from entitites.fire import Fire
        from entitites.bonus import Bonus
        from entitites.obstacle import Obstacle

        if not self.alive():
            return

        if self.type == 1:
            self.move_px(*tuple(x * self.speed for x in globals.BFS_DIRECTIONS[self.direction]))
            collisions = Collidable.get_collisions(self)
            self.spawn_bomb()
            for entity in collisions:
                if not isinstance(entity, Bonus) and not (isinstance(entity, Bomb) and entity.spawner == self):
                    self.move_px(*tuple(-x * self.speed for x in globals.BFS_DIRECTIONS[self.direction]))
                    self.direction ^= 2  # 0 to 2, 2 to 0, 1 to 3, 3 to 1 (UP <-> DOWN, LEFT <-> RIGHT)
                    break

            if rand(0, 500) < 5: # to simulate randomness like in actual game
                self.direction ^= 1

        elif 2 <= self.type <= 3:
            # print(self.moving, self.dest_x, self.dest_y, self.x, self.y)
            # self.type = 2: In this algorithm, bot moves into direction of the farthest cell from all bombs, fires and players. So, it just wanders
            # self.type = 3: Bot moves into direction of the closest player, trying to be far from bombs and fires. So, it is aggressive
            if self.moving == 1:
                # print(self.x, self.y)
                nx, ny = self.prev[self.x][self.y]
                if nx - self.x == 1:
                    self.direction = 1
                elif nx - self.x == -1:
                    self.direction = 3
                elif ny - self.y == 1:
                    self.direction = 2
                elif ny - self.y == -1:
                    self.direction = 0
                else:
                    self.moving = 0
                # print(f"from ({self.x}, {self.y}) to ({nx}, {ny}). Direction - {self.direction}. Goal is {self.dest_x}, {self.dest_y}")

                self.move_px(*tuple(x * self.speed for x in globals.BFS_DIRECTIONS[self.direction]))
                collisions = Collidable.get_collisions(self)
                for entity in collisions:
                    if ((not isinstance(entity, Player) and not isinstance(entity, Bonus) and not (isinstance(entity, Bomb) and entity.spawner == self))
                            or not in_valid_range(self.x, self.y, globals.cols, globals.rows)):
                        self.move_px(*tuple(-x * self.speed for x in globals.BFS_DIRECTIONS[self.direction]))
                        self.moving = 2
                        break

                self.x, self.y = get_pos(self.px_x, self.px_y)

            if self.moving == 2:
                cur_px_x, cur_px_y = get_field_pos(self.x, self.y)
                dx, dy = cur_px_x - self.px_x, cur_px_y - self.px_y
                if dx > self.speed:
                    dx = self.speed
                if dx < -self.speed:
                    dx = -self.speed
                if dy > self.speed:
                    dy = self.speed
                if dy < -self.speed:
                    dy = -self.speed
                if dx == 0 and dy == 0:
                    self.moving = 0
                self.move_px(dx, dy)
                self.x, self.y = get_pos(self.px_x, self.px_y)

            if self.moving == 0:
                queue = []
                bombs_lst = list(get_bombs(globals.entities))
                self.used = [
                    [False for j in range(globals.rows)] for i in range(globals.cols)
                ]
                self.blocked = [
                    [False for j in range(globals.rows)] for i in range(globals.cols)
                ]
                self.dist = [
                    [0 for j in range(globals.rows)] for i in range(globals.cols)
                ]
                self.prev = [
                    [(-1, -1) for j in range(globals.rows)] for i in range(globals.cols)
                ]
                for bomb in bombs_lst:
                    for fx in range(1, globals.cols - 1):
                        for fy in range(1, globals.rows - 1):
                            if abs(bomb.x - fx) + abs(bomb.y - fy) <= bomb.power:
                                self.used[fx][fy] = True
                                self.dist[fx][fy] = 0
                                self.prev[fx][fy] = (fx, fy)

                for entity in list(globals.entities):
                    if isinstance(entity, Bomb) or isinstance(entity, Fire) or (self.type == 2 and isinstance(entity, Player)):
                        x, y = entity.x, entity.y
                        if x < 0 or x >= globals.cols or y < 0 or y >= globals.rows:
                            continue

                        self.used[x][y] = True
                        self.dist[x][y] = 0
                        self.prev[x][y] = (x, y)

                    if isinstance(entity, Obstacle):
                        x, y = entity.x, entity.y
                        if x < 0 or x >= globals.cols or y < 0 or y >= globals.rows:
                            continue
                        self.blocked[x][y] = True

                for x in range(globals.cols):
                    for y in range(globals.rows):
                        if self.used[x][y]:
                            queue.append((x, y))
                def bfs():
                    while queue:
                        x, y = queue[0]
                        queue.pop(0)
                        for dx, dy in globals.BFS_DIRECTIONS:
                            nx, ny = x + dx, y + dy
                            if nx < 0 or nx >= globals.cols or ny < 0 or ny >= globals.rows:
                                continue
                            if self.blocked[nx][ny]:
                                continue
                            if not self.used[nx][ny]:
                                self.used[nx][ny] = True
                                self.prev[nx][ny] = (x, y)
                                self.dist[nx][ny] = self.dist[x][y] + 1
                                queue.append((nx, ny))

                bfs()

                if self.type == 2:
                    dst = -1
                    farthest = []
                    for x in range(globals.cols):
                        for y in range(globals.rows):
                            if not self.blocked[x][y] and self.used[x][y] and self.prev[x][y] != (-1, -1):
                                if self.dist[x][y] > dst:
                                    dst = self.dist[x][y]


                    for x in range(globals.cols):
                        for y in range(globals.rows):
                            if not self.blocked[x][y] and self.used[x][y] and self.prev[x][y] != (-1, -1):
                                if self.dist[x][y] >= dst - 5:
                                    # If we left just dst, then in situation where one player moves too fast,
                                    # the bot would have to move across the entire playing field, which would be disadvantageous for bot.
                                    # So, dst-5 is required to avoid potentially disadvantageous routes
                                    farthest.append((x, y))

                    if (self.dest_x, self.dest_y) not in farthest and len(farthest) > 0:
                        # if current goal is already one of the best options, then we don't update
                        nx, ny = farthest[rand(0, len(farthest))]
                        self.dest_x, self.dest_y = nx, ny
                        self.dest_px_x, self.dest_px_y = get_field_pos(nx, ny)

                else:
                    dst = float('inf')
                    for player in list(get_players(globals.entities)):
                        x, y = player.x, player.y
                        if in_valid_range(x, y, globals.cols, globals.rows) and self.dist[x][y] < dst:
                            dst = self.dist[x][y]
                            nx, ny = x, y

                    if dst < float('inf'):
                        self.dest_x, self.dest_y = nx, ny
                        self.dest_px_x, self.dest_px_y = get_field_pos(nx, ny)

                if dst < self.bomb_power:
                    self.spawn_bomb()

                # path from destination to bot
                queue = [(self.dest_x, self.dest_y)]

                self.used = [
                    [False for j in range(globals.rows)] for i in range(globals.cols)
                ]
                self.used[self.dest_x][self.dest_y] = True
                self.dist = [
                    [0 for j in range(globals.rows)] for i in range(globals.cols)
                ]
                self.prev = [
                    [(-1, -1) for j in range(globals.rows)] for i in range(globals.cols)
                ]
                self.prev[self.dest_x][self.dest_y] = (self.dest_x, self.dest_y)
                bfs()
                self.moving = 1

        else:
            raise Exception("Unknown type of bot!")

def get_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bot):
            res.add(entity)
    return res