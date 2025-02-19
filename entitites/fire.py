from entitites.bot import Bot
from entitites.entity import Entity
import pages.game.game
from entitites.obstacle import Obstacle
from utils.helpers import get_ms_from_tick
import globals

class Fire(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.power = kwargs.get("power", 1)
        self.timer = kwargs.get("timer", 300)
        self.spawner = kwargs.get("spawner", None)  # which entity spawned
        self.type = "bfs"# | "right"


    def add_tick(self):
        self.tick += 1
        if self.mounted and get_ms_from_tick(self.tick) > self.timer:
            self.self_destroy()

    def self_destroy(self):
        self.unmount()

        if self.entity_group:
            self.entity_group.discard(self)

    def explosion(self, power):
        if power < 1:
            return
        self.power = power
        for dx, dy in globals.directions:
            nx = self.x + dx
            ny = self.y + dy
            if nx < 0 or nx > globals.rows or ny < 0 or ny > globals.cols:
                continue
            fire = Fire(
                spawner=self,
                px_w=self.px_w,
                px_h=self.px_h,
                px_x=self.px_x + dx * globals.cell_size,
                px_y=self.px_y + dy * globals.cell_size,
                x=nx,
                y=ny,
                layer=self.layer + 1,
                color=self.color,
                power=self.power + 1,
                entity_group=globals.entities,
            )
            collision = False
            entity_lst = list(globals.entities)
            for entity in entity_lst:
                if entity.x != nx or entity.y != ny:
                    continue
                if isinstance(entity, Bot):
                    entity.unmount()
                    globals.entities.remove(entity)
                elif isinstance(entity, Obstacle):
                    if entity.type == globals.U_OBSTACLE_CELL:
                        collision = True
                    else:  # destroyable
                        entity.unmount()
                        globals.entities.remove(entity)

            if collision:
                fire.unmount()
                continue

            fire.mount()
            fire.explosion(power - 1)

    #TODO: directional explosion etc.