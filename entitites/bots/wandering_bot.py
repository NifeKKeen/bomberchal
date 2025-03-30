from entitites.bot import Bot
from entitites.fire import get_fires
from entitites.interfaces.Collidable import Collidable
from utils.helpers import get_pos, get_field_pos, in_valid_range, rand
import globals
from heapq import heappush, heappop


WANDERING_BOT_KEY = "wandering_bot"


class WanderingBot(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.entity_key = WANDERING_BOT_KEY

        self.map_allowed_bonus_types[globals.BONUS_CAPACITY] = False
        self.map_allowed_bonus_types[globals.BONUS_POWER] = False
        self.texture_type = "wandering"
        self.set_image_path(globals.bot_frames[self.texture_type]["top_static"][0])

    def think(self):
        from entitites.player import Player
        from entitites.bomb import Bomb
        from entitites.bomb import get_bombs
        from entitites.fire import Fire
        from entitites.bonus import Bonus
        from entitites.obstacle import Obstacle

        if not self.alive():
            return

        # In this algorithm, bot moves into direction of the destinations cell from all bombs, fires and players. So, it just wanders

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
            else:  # if nx and ny are not changing or if there is some error
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
                if self.dest_x == self.x and self.dest_y == self.y:
                    self.moving = 0
                else:
                    self.moving = 1

            self.move_px(dx, dy)
            self.x, self.y = get_pos(self.px_x, self.px_y)

        if self.moving == 0:
            queue = []
            bombs_lst = list(get_bombs(globals.entities)) + list(get_fires(globals.entities))
            for x in range(globals.cols):
                for y in range(globals.rows):
                    self.used[x][y] = False
                    self.weight[x][y] = 0
                    self.dist[x][y] = globals.inf
                    self.weighted_dist[x][y] = 0
                    self.prev[x][y] = (-1, -1)

            def add(x, y):
                heappush(queue, ((self.weighted_dist[x][y], self.dist[x][y]), (x, y)))

            for bomb in bombs_lst:
                for fx in range(max(1, bomb.x - bomb.power), min(globals.cols - 1, bomb.x + bomb.power + 1)):
                    for fy in range(max(1, bomb.y - bomb.power), min(globals.rows - 1, bomb.y + bomb.power + 1)):
                        if abs(bomb.x - fx) + abs(bomb.y - fy) <= bomb.power:
                            self.weight[fx][fy] += bomb.power - (abs(bomb.x - fx) + abs(bomb.y - fy)) + 1

            for entity in list(globals.entities):
                if isinstance(entity, Fire):
                    x, y = int(entity.x), int(entity.y)
                    if not in_valid_range(x, y, globals.cols, globals.rows):
                        continue
                    self.weight[x][y] += 10

                if isinstance(entity, Player):
                    x, y = int(entity.x), int(entity.y)
                    if not in_valid_range(x, y, globals.cols, globals.rows):
                        continue
                    self.weight[x][y] += entity.bomb_power + 5

                if isinstance(entity, Obstacle) or (isinstance(entity, Bot) and entity != self):
                    x, y = int(entity.x), int(entity.y)
                    if not in_valid_range(x, y, globals.cols, globals.rows):
                        continue
                    self.weight[x][y] = globals.inf

            if in_valid_range(self.x, self.y, globals.cols, globals.rows):
                self.weighted_dist[self.x][self.y] = self.weight[self.x][self.y]
                self.dist[self.x][self.y] = 0
                add(self.x, self.y)

            def dijkstra():
                while queue:
                    (cur_weighted_dist, cur_dist), (x, y) = heappop(queue)
                    if self.used[x][y]:  # skipping disadvantageous distances
                        continue
                    self.used[x][y] = True

                    for dx, dy in globals.BFS_DIRECTIONS:
                        nx, ny = x + dx, y + dy
                        if not in_valid_range(nx, ny, globals.cols, globals.rows):
                            continue
                        if self.weight[x][y] == globals.inf:
                            continue

                        new_weighted_dist = max(cur_weighted_dist, self.weight[nx][ny])
                        new_dist = cur_dist + 1

                        if (self.weighted_dist[nx][ny] > new_weighted_dist or
                                (self.weighted_dist[nx][ny] == new_weighted_dist and self.dist[nx][ny] > new_dist)):
                            self.weighted_dist[nx][ny] = new_weighted_dist
                            self.dist[nx][ny] = new_dist
                            self.prev[nx][ny] = (x, y)
                            add(nx, ny)

                        elif self.dist[nx][ny] > new_dist:
                            self.weighted_dist[nx][ny] = new_weighted_dist
                            self.dist[nx][ny] = new_dist
                            self.prev[nx][ny] = (x, y)
                            add(nx, ny)

            dijkstra()
            min_dist = globals.inf
            max_dist = float('-inf')
            min_weighted_dist = globals.inf
            destinations = []
            for x in range(globals.cols):
                for y in range(globals.rows):
                    if self.used[x][y]:
                        if self.weighted_dist[x][y] < min_weighted_dist:
                            min_weighted_dist = self.weighted_dist[x][y]

            for x in range(globals.cols):
                for y in range(globals.rows):
                    if self.used[x][y] and self.weighted_dist[x][y] == min_weighted_dist:
                        if self.dist[x][y] < min_dist:
                            min_dist = self.dist[x][y]
                        if self.dist[x][y] > max_dist:
                            max_dist = self.dist[x][y]

            for x in range(globals.cols):
                for y in range(globals.rows):
                    if self.used[x][y] and self.weighted_dist[x][y] == min_weighted_dist:
                        if self.dist[x][y] >= max_dist - 5:
                            # max_dist-5 to avoid sometimes disadvantageous routes
                            destinations.append((x, y))

            if (self.dest_x, self.dest_y) not in destinations and destinations:
                # if current goal is already one of the best options, then we don't update
                nx, ny = destinations[rand(0, len(destinations))]
                self.dest_x, self.dest_y = nx, ny
                self.dest_px_x, self.dest_px_y = get_field_pos(nx, ny)

            queue.clear()
            for x in range(globals.cols):
                for y in range(globals.rows):
                    self.used[x][y] = False
                    self.dist[x][y] = globals.inf
                    self.weighted_dist[x][y] = 0
                    self.prev[x][y] = (-1, -1)
            self.weighted_dist[self.dest_x][self.dest_y] = self.weight[self.dest_x][self.dest_y]
            self.dist[self.dest_x][self.dest_y] = 0

            self.prev[self.dest_x][self.dest_y] = (self.dest_x, self.dest_y)
            add(self.dest_x, self.dest_y)
            dijkstra()

            self.moving = 1


def get_wandering_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, WanderingBot):
            res.add(entity)
    return res
