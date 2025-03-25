import globals
from utils.helpers import get_tick_from_ms, in_valid_range, rand
from entitites.entity import Entity
from entitites.interfaces.Collidable import Collidable


class Fire(Collidable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_ENTITY_LAYER + 8

        self.power = kwargs.get("power", 1)
        self.timer = kwargs.get("timer", get_tick_from_ms(300))
        self.spread_timer = kwargs.get("spread_timer", get_tick_from_ms(0))
        self.spawner = kwargs.get("spawner", None)  # which entity spawned
        self.is_initial = kwargs.get("is_initial", False)
        self.spread_type = kwargs.get("spread_type", "bfs")  # | "star" | "up" | "right" | "down" | "left"
        self.did_spread = False

        if self.mounted:
            globals.field_fire_state[self.x][self.y] = self.power
            self.set_image_path(globals.explosion_frames[0])
            if self.spread_timer == 0:
                self.handle_collision()


    def add_tick(self):
        self.tick += 1
        if not self.mounted:
            return

        if not self.did_spread and self.tick > self.spread_timer:
            self.spread()

        if self.tick > self.timer:
            self.self_destroy()
            return

        if self.tick < self.timer // 3:
            self.set_image_path(globals.explosion_frames[0])
        elif self.tick < (self.timer // 3) * 2:
            self.px_w = self.image_size[0] - 2
            self.px_h = self.image_size[1] - 2
            self.set_image_path(globals.explosion_frames[1])
        else:
            self.px_w = self.image_size[0] - 6
            self.px_h = self.image_size[1] - 6
            self.set_image_path(globals.explosion_frames[2])

    def self_destroy(self):
        globals.field_fire_state[self.x][self.y] = 0
        self.kill()

    def spread_bfs(self):
        directions = globals.BFS_DIRECTIONS
        for dx, dy in directions:
            nx = self.x + dx
            ny = self.y + dy
            if (self.power - 1 <= 0 or
                not in_valid_range(nx, ny, len(globals.field_fire_state), len(globals.field_fire_state[0]))
            ):
                continue

            # if globals.field_fire_state[nx][ny] >= self.power - 1:
            #     continue
            if globals.field_fire_state[nx][ny] and (rand(0, 2) or globals.field_fire_state[nx][ny] >= self.power - 1):  # with 50% chance it the fire with higher power will proceed
                continue

            new_fire = Fire(  #region parameters
                is_initial=False,
                power=self.power - 1,
                timer=self.timer,
                spread_timer=self.spread_timer,
                spawner=self.spawner,
                spread_type=self.spread_type,

                x=nx,
                y=ny,
                px_x=self.px_x + dx * globals.CELL_SIZE,
                px_y=self.px_y + dy * globals.CELL_SIZE,
                px_w=self.px_w,
                px_h=self.px_h,

                color=self.color,
                entity_group=globals.entities,
            )  #endregion

            if new_fire.spread_timer == 0:
                new_fire.spread()

    def spread_star(self):
        for spread_type, (dx, dy) in globals.MAP_DIRECTION.items():
            nx = self.x + dx
            ny = self.y + dy
            if not in_valid_range(nx, ny, len(globals.field_fire_state), len(globals.field_fire_state[0])):
                continue

            new_fire = Fire(  #region parameters
                is_initial=False,
                power=self.power - 1,
                timer=self.timer,
                spread_timer=self.spread_timer,
                spawner=self.spawner,
                spread_type=spread_type,

                x=nx,
                y=ny,
                px_x=self.px_x + dx * globals.CELL_SIZE,
                px_y=self.px_y + dy * globals.CELL_SIZE,
                px_w=self.px_w,
                px_h=self.px_h,

                color=self.color,
                entity_group=globals.entities,
            )  #endregion

            if new_fire.spread_timer == 0:
                new_fire.spread()

    def spread_straight(self):
        dx, dy = globals.MAP_DIRECTION[self.spread_type]
        nx = self.x + dx
        ny = self.y + dy
        if not in_valid_range(nx, ny, len(globals.field_fire_state), len(globals.field_fire_state[0])):
            return

        new_fire = Fire(  #region parameters
            is_initial=False,
            power=self.power - 1,
            timer=self.timer,
            spread_timer=self.spread_timer,
            spawner=self.spawner,
            spread_type=self.spread_type,

            x=nx,
            y=ny,
            px_x=self.px_x + dx * globals.CELL_SIZE,
            px_y=self.px_y + dy * globals.CELL_SIZE,
            px_w=self.px_w,
            px_h=self.px_h,

            color=self.color,
            entity_group=globals.entities,
        )  #endregion

        if new_fire.spread_timer == 0:
            new_fire.spread()

    def spread(self):
        if not self.mounted:
            return

        if self.power < 1 or self.did_spread:
            return
        self.did_spread = True

        if self.spread_type == "bfs":
            self.spread_bfs()
        elif self.spread_type == "star":
            self.spread_star()
        elif self.spread_type in globals.MAP_DIRECTION:
            self.spread_straight()
        else:
            raise Exception("Unknown type of spread!")
