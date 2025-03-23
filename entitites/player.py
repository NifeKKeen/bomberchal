import globals
from utils.helpers import get_tick_from_ms
from entitites.entity import Entity
from entitites.interfaces.BombSpawnable import BombSpawnable
from entitites.interfaces.Collidable import Collidable
from entitites.interfaces.Controllable import Controllable
from entitites.interfaces.Movable import Movable


class Player(Collidable, Controllable, BombSpawnable, Movable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._layer = globals.BASE_ENTITY_LAYER + 5

        self.damage_countdown = kwargs.get("damage_countdown", get_tick_from_ms(3000))
        self.bonuses = kwargs.get("bonuses", [])  # BonusItem instances
        self.character_skin_key = kwargs.get("character_skin_key", "ch1")

        self.image_size = self.px_w + 16, self.px_h
        self.set_image_path(globals.character_frames[self.character_skin_key]["top_static"][0])

    def add_tick(self):
        self.tick += 1
        if self.moved_this_frame:
            image_key = f"{self.last_direction}_moving"
            idx = (self.tick // 8) % len(globals.character_frames[self.character_skin_key][image_key])
            self.set_image_path(globals.character_frames[self.character_skin_key][image_key][idx])
        else:
            image_key = f"{self.last_direction}_static"
            idx = (self.tick // 8) % len(globals.character_frames[self.character_skin_key][image_key])
            self.set_image_path(globals.character_frames[self.character_skin_key][image_key][idx])

        if self.cur_damage_countdown > 0:
            self.hidden = self.cur_damage_countdown % 8 < 4
        else:
            self.hidden = False

        # FOR TESTING
        # if self.moved_this_frame:
        #     image_key = f"{self.last_direction}_moving"
        #     idx = (self.tick // 8) % len(globals.bot_frames["wandering"][image_key])
        #     self.set_image_path(globals.bot_frames["wandering"][image_key][idx])
        # else:
        #     image_key = f"{self.last_direction}_static"
        #     idx = (self.tick // 8) % len(globals.bot_frames["wandering"][image_key])
        #     self.set_image_path(globals.bot_frames["wandering"][image_key][idx])

    # def kill(self):  # noclip
    #     return


def get_players(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Player):
            res.add(entity)
    return res
