from entitites.bots.aggressive_bot import AggressiveBot

class BossBot(AggressiveBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

def get_boss_bots(entities):
    res = set()
    for entity in entities:
        if isinstance(entity, BossBot):
            res.add(entity)
    return res
