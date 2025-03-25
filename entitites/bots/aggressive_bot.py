from entitites.bot import Bot
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.Collidable import Collidable
from utils.helpers import get_pos, get_field_pos, in_valid_range
import globals


class AggressiveBot(Bot, BombSpawnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.texture_type = "aggressive"
        self.set_image_path(globals.bot_frames[self.texture_type]["top_static"][0])

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
        if self.moving == 1:
            if in_valid_range(self.x, self.y, globals.cols, globals.rows):
                nx, ny = self.prev[self.x][self.y]
            else:
                nx, ny = -1, -1

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
            self.blocked = [
                [False for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            self.dist = [
                [0 for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            self.prev = [
                [(-1, -1) for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            for bomb in bombs_lst:
                for fx in range(1, globals.cols - 1):
                    for fy in range(1, globals.rows - 1):
                        if abs(bomb.x - fx) + abs(bomb.y - fy) <= bomb.power:
                            self.used[fx][fy] = True
                            self.dist[fx][fy] = 0
                            self.prev[fx][fy] = (fx, fy)

            for entity in list(globals.entities):
                if isinstance(entity, Bomb) or isinstance(entity, Fire):
                    x, y = entity.x, entity.y
                    if not in_valid_range(x, y, globals.cols, globals.rows):
                        continue

                    self.used[x][y] = True
                    self.dist[x][y] = 0
                    self.prev[x][y] = (x, y)

                if isinstance(entity, Obstacle):
                    x, y = entity.x, entity.y
                    if not in_valid_range(x, y, globals.cols, globals.rows):
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
            dst = float('inf')
            nx, ny = 1, 1
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
                [False for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            self.used[self.dest_x][self.dest_y] = True
            self.dist = [
                [0 for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            self.prev = [
                [(-1, -1) for _ in range(globals.rows)] for _ in range(globals.cols)
            ]
            self.prev[self.dest_x][self.dest_y] = (self.dest_x, self.dest_y)
            bfs()
            self.moving = 1

def get_aggressive_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, AggressiveBot):
            res.add(entity)
    return res
