from entitites.bot import Bot
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.Collidable import Collidable
from utils.helpers import get_pos, get_field_pos, in_valid_range, get_tick_from_ms, rand
import globals
from heapq import heappush, heappop


class AggressiveBot(Bot, BombSpawnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.texture_type = "aggressive"
        self.set_image_path(globals.bot_frames[self.texture_type]["top_static"][0])
        self.boredom_countdown = kwargs.get("boredom_countdown", 0)
        self.cur_boredom_countdown = kwargs.get("cur_boredom_countdown", 0)
        self.cur_boredom_countdown = self.boredom_countdown

    def think(self):
        from entitites.player import Player, get_players
        from entitites.bomb import Bomb
        from entitites.bomb import get_bombs
        from entitites.fire import Fire
        from entitites.bonus import Bonus
        from entitites.obstacle import Obstacle

        if not self.alive():
            return

        # In this algorithm, bot moves into direction of the closest player, trying to be far from bombs and fires. So, it is aggressive
        # If bot is unable to reach any player, it will walk within reachable cells
        # If bot can't find path to player in [3; 50] seconds, it will get bored and spawn bomb
        # TODO: If bot is unable to reach any player, but can safely spawn bomb to break obstacles, it should do that.
        # TODO: Otherwise, if then bomb will damage bot, it will walk within reachable cells

        if len(get_players(globals.entities)) == 0:
            # Just for fun
            self.cur_bomb_countdown = 0
            self.spawn_bomb()

        elif self.boredom_countdown <= 0:
            self.spawn_bomb()
            self.cur_boredom_countdown = self.boredom_countdown

        if self.moving == 1:
            if in_valid_range(self.x, self.y, globals.cols, globals.rows):
                nx, ny = self.prev[self.x][self.y]
            else:
                nx, ny = -1, -1
            # print(f"lets move from ({self.x}, {self.y}) to ({nx}, {ny}). Final destination: ({self.dest_x}, {self.dest_y})")

            if nx - self.x == 1:
                self.direction = 1
            elif nx - self.x == -1:
                self.direction = 3
            elif ny - self.y == 1:
                self.direction = 2
            elif ny - self.y == -1:
                self.direction = 0
            else: # if nx and ny are not changing or if there is some error
                self.moving = 0

            self.move_px(*tuple(x * self.speed for x in globals.BFS_DIRECTIONS[self.direction]))
            collisions = Collidable.get_collisions(self)
            for entity in collisions:
                if ((not isinstance(entity, Player) and not isinstance(entity, Bonus) and not (isinstance(entity, Bomb) and entity.spawner_key == self.key))
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
                [False for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            self.weight = [
                [0 for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            self.dist = [
                [float('inf') for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            self.prev = [
                [(-1, -1) for _ in range(globals.rows)] for _ in range(globals.cols)
            ]

            def add(x, y):
                heappush(queue, (self.dist[x][y], (x, y)))

            # self.spawn_bomb(is_simulation=True)

            for bomb in bombs_lst:
                for fx in range(1, globals.cols - 1):
                    for fy in range(1, globals.rows - 1):
                        # TODO: Peredelat' na is_simulation
                        if abs(bomb.x - fx) + abs(bomb.y - fy) <= bomb.power:
                            self.weight[fx][fy] = bomb.power + 1 - abs(bomb.x - fx) + abs(bomb.y - fy)
                            # self.used[fx][fy] = True
                            # self.dist[fx][fy] = 0
                            # self.prev[fx][fy] = (fx, fy)

            for entity in list(globals.entities):
                if isinstance(entity, Fire):
                    x, y = entity.x, entity.y
                    if not in_valid_range(x, y, globals.cols, globals.rows):
                        continue

                    self.weight[x][y] = 10
                    # self.used[x][y] = True
                    # self.dist[x][y] = 0
                    # self.prev[x][y] = (x, y)

                if isinstance(entity, Obstacle) or (isinstance(entity, Bot) and entity != self):
                    x, y = entity.x, entity.y
                    if not in_valid_range(x, y, globals.cols, globals.rows):
                        continue
                    self.weight[x][y] = float('inf')
            #
            # for x in range(globals.cols):
            #     for y in range(globals.rows):
            #         if self.used[x][y]:
            #             add(x, y)

            if in_valid_range(self.x, self.y, globals.cols, globals.rows):
                self.dist[self.x][self.y] = self.weight[self.x][self.y]
                add(self.x, self.y)

            def dijkstra():
                while queue:
                    cur_dist, (x, y) = heappop(queue)
                    if self.used[x][y]: # skipping disadvantageous distances
                        continue
                    self.used[x][y] = True

                    for dx, dy in globals.BFS_DIRECTIONS:
                        nx, ny = x + dx, y + dy
                        if not in_valid_range(nx, ny, globals.cols, globals.rows):
                            continue
                        if self.weight[x][y] == float('inf'):
                            continue

                        new_dist = self.dist[x][y] + self.weight[nx][ny] + 1
                        if self.dist[nx][ny] > new_dist:
                            self.dist[nx][ny] = new_dist
                            self.prev[nx][ny] = (x, y)
                            add(nx, ny)

            dijkstra()
            dst = float('inf')
            nx, ny = 1, 1

            for player in list(get_players(globals.entities)):
                x, y = player.x, player.y
                if in_valid_range(x, y, globals.cols, globals.rows) and self.used[x][y] and self.dist[x][y] < dst:
                    dst = self.dist[x][y]
                    nx, ny = x, y

            if dst < float('inf'): # there is player that can be reached
                self.dest_x, self.dest_y = nx, ny
                self.dest_px_x, self.dest_px_y = get_field_pos(nx, ny)

                if dst < self.bomb_power:
                    # print(dst, self.bomb_power)
                    self.spawn_bomb()
                    self.moving = 0
                else:
                    self.moving = 1

                # path from destination to bot
                queue = []

                self.used = [
                    [False for _ in range(globals.rows)] for _ in range(globals.cols)
                ]
                self.dist = [
                    [float('inf') for _ in range(globals.rows)] for _ in range(globals.cols)
                ]
                self.prev = [
                    [(-1, -1) for _ in range(globals.rows)] for _ in range(globals.cols)
                ]
                self.dist[self.dest_x][self.dest_y] = self.weight[self.dest_x][self.dest_y]
                self.prev[self.dest_x][self.dest_y] = (self.dest_x, self.dest_y)
                add(self.dest_x, self.dest_y)
                dijkstra()

            else: # checking whether bomb can be spawned to leave
                dst = 0
                for x in range(globals.cols):
                    for y in range(globals.rows):
                        # print(x, y, self.dist[x][y])
                        if self.used[x][y] and dst <= self.dist[x][y] < float('inf'):
                            dst = self.dist[x][y]
                            self.dest_x, self.dest_y = x, y
                
                queue = []

                self.used = [
                    [False for _ in range(globals.rows)] for _ in range(globals.cols)
                ]
                self.dist = [
                    [float('inf') for _ in range(globals.rows)] for _ in range(globals.cols)
                ]
                self.prev = [
                    [(-1, -1) for _ in range(globals.rows)] for _ in range(globals.cols)
                ]
                self.dist[self.dest_x][self.dest_y] = self.weight[self.dest_x][self.dest_y]
                self.prev[self.dest_x][self.dest_y] = (self.dest_x, self.dest_y)
                add(self.dest_x, self.dest_y)
                dijkstra()
                

                # print(self.x, self.y, dst, self.dest_x, self.dest_y, self.dist[self.dest_x][self.dest_y])
                self.moving = 1
                # self.spawn_bomb(is_simulation=True)

def get_aggressive_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, AggressiveBot):
            res.add(entity)
    return res
