from entitites.entity import Entity
from entitites.interfaces.Collidable import Collidable
from utils.helpers import get_ms_from_tick, get_tick_from_ms, in_valid_range
import globals

class Fire(Collidable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.power = kwargs.get("power", 1)
        self.timer = kwargs.get("timer", 300)
        self.spread_timer = kwargs.get("spread_timer", 0)
        self.spawner = kwargs.get("spawner", None)  # which entity spawned
        self.is_initial = kwargs.get("is_initial", False)
        self.type = kwargs.get("type", "bfs")  # | "star" | "up" | "right" | "down" | "left"
        self.fired = False
        if self.mounted:
            globals.field_fire_state[self.x][self.y] = self.power
            if self.spread_timer == 0:
                self.handle_collision()


    def add_tick(self):
        self.tick += 1
        if self.mounted and not self.fired and get_ms_from_tick(self.tick) > self.spread_timer:
            self.spread()

        if self.mounted and get_ms_from_tick(self.tick) > self.timer:
            self.self_destroy()

    def self_destroy(self):
        globals.field_fire_state[self.x][self.y] = 0
        self.kill()

    def spread_bfs(self):
        directions = globals.BFS_DIRECTIONS
        for dx, dy in directions:
            nx = self.x + dx
            ny = self.y + dy
            if self.power - 1 <= 0 or not in_valid_range(nx, ny, globals.rows, globals.cols):
                continue

            if globals.field_fire_state[nx][ny] >= self.power:
                continue

            if globals.field[nx][ny] == globals.U_OBSTACLE_CELL:
                continue

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
                layer=self.layer,
                color=self.color,
                entity_group=globals.entities,
            )

            if new_fire.spread_timer == 0:
                new_fire.spread()

    def spread_star(self):
        for spread_type, (dx, dy) in globals.MAP_DIRECTION.items():
            nx = self.x + dx
            ny = self.y + dy
            if not in_valid_range(nx, ny, globals.rows, globals.cols):
                continue
            if globals.field[nx][ny] == globals.U_OBSTACLE_CELL:
                continue

            new_fire = Fire(
                mounted=True,
                is_initial=False,
                power=self.power - 1,
                timer=self.timer,
                spread_timer=self.spread_timer,
                spawner=self.spawner,
                type=spread_type,
                px_w=self.px_w,
                px_h=self.px_h,
                px_x=self.px_x + dx * globals.cell_size,
                px_y=self.px_y + dy * globals.cell_size,
                x=nx,
                y=ny,
                layer=self.layer,
                color=self.color,
                entity_group=globals.entities,
            )

            if new_fire.spread_timer == 0:
                new_fire.spread()

    def spread_straight(self):
        dx, dy = globals.MAP_DIRECTION[self.type]
        nx = self.x + dx
        ny = self.y + dy
        if not in_valid_range(nx, ny, globals.rows, globals.cols):
            return
        if globals.field[nx][ny] == globals.U_OBSTACLE_CELL:
            return

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
            layer=self.layer,
            color=self.color,
            entity_group=globals.entities,
        )

        if new_fire.spread_timer == 0:
            new_fire.spread()

    def spread(self):
        if not self.mounted:
            return

        if self.power < 1 or self.fired:
            return
        self.fired = True

        if self.type == "bfs":
            self.spread_bfs()
        elif self.type == "star":
            self.spread_star()
        elif self.type in globals.MAP_DIRECTION:
            self.spread_straight()
        else:
            raise Exception("Unknown type of spread!")
