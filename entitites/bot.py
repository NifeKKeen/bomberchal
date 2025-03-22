import globals
from utils.helpers import rand
from entitites.entity import Entity
from entitites.interfaces.BotIntellect import BotIntellect
from entitites.interfaces.Movable import Movable


class Bot(BotIntellect, Movable, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonuses = kwargs.get("bonuses", [])  # BonusItem instances

    def add_tick(self):
        self.tick += 1
        if rand(1, 1000) <= 0: # test
            self.spawn_bomb()

        if self.moved_this_frame:
            image_key = f"{self.last_direction}_moving"
            idx = (self.tick // 8) % len(globals.bot_frames["wandering"][image_key])
            self.set_image_path(globals.bot_frames["wandering"][image_key][idx])
        else:
            image_key = f"{self.last_direction}_static"
            idx = (self.tick // 8) % len(globals.bot_frames["wandering"][image_key])
            self.set_image_path(globals.bot_frames["wandering"][image_key][idx])

        if self.cur_damage_countdown > 0:
            self.hidden = self.cur_damage_countdown % 8 < 4
        else:
            self.hidden = False

def get_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, Bot):
            res.add(entity)
    return res