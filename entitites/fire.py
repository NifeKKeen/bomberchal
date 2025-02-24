from entitites.bot import Bot
from entitites.entity import Entity
import pages.game.game
from entitites.obstacle import Obstacle
from utils.helpers import get_ms_from_tick
import globals

class Fire(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.power = kwargs.get("power", 5)
        self.timer = kwargs.get("timer", 300)
        self.spawner = kwargs.get("spawner", None)  # which entity spawned
        self.type = "bfs" # | "directional0" | "directional1" | "directional2" | "directional3"
        self.exploded = False
        self.initial_fire_key = kwargs.get("initial_fire_key", None)
        if self.initial_fire_key:
            self.key = f"f-{self.entity_id}"

    def add_tick(self):
        self.tick += 1
        if self.mounted and get_ms_from_tick(self.tick) > self.timer:
            self.spread()
            self.self_destroy()

    def self_destroy(self):
        self.unmount()

        if self.entity_group:
            self.entity_group.discard(self)

    def spread(self):
        directions = []
        if self.power < 1 or self.exploded:
            return
        self.exploded = True
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
            if nx < 0 or nx >= globals.rows or ny < 0 or ny >= globals.cols:
                continue
            if dx == 1 and self.x < self.spawner.x:
                continue
            if dx == -1 and self.x > self.spawner.x:
                continue
            if dy == 1 and self.y < self.spawner.y:
                continue
            if dy == -1 and self.y > self.spawner.y:
                continue

            new_fire = Fire(
                spawner=self.spawner,
                px_w=self.px_w,
                px_h=self.px_h,
                px_x=self.px_x + dx * globals.cell_size,
                px_y=self.px_y + dy * globals.cell_size,
                x=nx,
                y=ny,
                layer=self.layer + 1,
                color=self.color,
                power=self.power - 1,
                timer=self.timer,
                type=self.type,
                entity_group=globals.entities,
                initial_fire_key=self.initial_fire_key
            )
            collision = False
            entity_lst = list(globals.entities)
            for entity in entity_lst:
                if entity.x != nx or entity.y != ny:
                    continue
                # They collide

                if isinstance(entity, Obstacle):
                    if entity.type == globals.U_OBSTACLE_CELL: # undestroyable
                        collision = True
                    else:  # destroyable
                        entity.kill()
                elif not isinstance(entity, Fire):
                    entity.kill()

            if collision:
                # self.self_destroy()
                continue

            new_fire.mount()
            new_fire.spread()
