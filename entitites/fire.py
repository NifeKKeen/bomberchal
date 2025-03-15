from entitites.entity import Entity
from entitites.interfaces.Collidable import Collidable
from utils.helpers import get_ms_from_tick, get_tick_from_ms
import globals

class Fire(Collidable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.power = kwargs.get("power", 5)
        self.timer = kwargs.get("timer", 300)
        self.spread_timer = kwargs.get("spread_timer", 0)
        self.spawner = kwargs.get("spawner", None)  # which entity spawned
        self.is_initial = kwargs.get("is_initial", False)
        self.type = "bfs" # | "directional0" | "directional1" | "directional2" | "directional3"
        self.fired = False

        if self.mounted and self.is_initial and (0 <= self.x <  globals.cols and 0 <= self.y <  globals.rows):
            globals.field_fire_state[self.x][self.y] = self.power

    def add_tick(self):
        self.tick += 1

        if self.mounted and not self.fired and get_ms_from_tick(self.tick) > self.spread_timer:
            self.spread()

        if self.mounted and get_ms_from_tick(self.tick) > self.timer:
            self.self_destroy()

    def self_destroy(self):
        if 0 <= self.x <  globals.cols and 0 <= self.y <  globals.rows:
            globals.field_fire_state[self.x][self.y] = 0
        self.kill()

    def spread(self):
        if self.power < 1 or self.fired:
            return
        self.fired = True

        if self.type == "bfs":
            directions = globals.directions
        elif self.type[:-1] == "directional":
            direction = int(self.type[-1])
            directions = [globals.directions[direction]]
        else:
            raise Exception("Unknown type of spread!")

        for dx, dy in directions:
            nx = self.x + dx
            ny = self.y + dy
            if nx < 0 or nx >= globals.cols or ny < 0 or ny >= globals.rows:
                continue

            if globals.field_fire_state[nx][ny] >= self.power:
                continue
            globals.field_fire_state[nx][ny] = self.power

            if globals.field[nx][ny] == globals.U_OBSTACLE_CELL:
                continue
            # if dx == 1 and self.x < self.spawner.x:
            #     continue
            # if dx == -1 and self.x > self.spawner.x:
            #     continue
            # if dy == 1 and self.y < self.spawner.y:
            #     continue
            # if dy == -1 and self.y > self.spawner.y:
            #     continue

            new_fire = Fire(
                mounted=True,
                is_initial=False,
                power=self.power - 1,
                timer=self.timer,
                spread_timer=self.spread_timer,
                spawner=self.spawner,
                type=self.type,
                px_w=self.px_w,
                px_h=self.px_h,
                px_x=self.px_x + dx * globals.cell_size,
                px_y=self.px_y + dy * globals.cell_size,
                x=nx,
                y=ny,
                layer=self.layer + 1,
                color=self.color,
                entity_group=globals.entities,
            )

            if self.spread_timer == 0:
                new_fire.spread()
