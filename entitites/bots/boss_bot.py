import globals
from entitites.bots.aggressive_bot import AggressiveBot


BOSS_BOT_KEY = "boss_bot"


class BossBot(AggressiveBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.entity_key = BOSS_BOT_KEY

        self.texture_type = "boss"
        self.set_image_path(globals.bot_frames[self.texture_type]["top_static"][0])


def get_boss_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, BossBot):
            res.add(entity)
    return res
