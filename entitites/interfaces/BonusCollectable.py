import globals
from entitites.entity import Entity


class BonusCollectable(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonus_keys = kwargs.get("bonuses", [])  # Bonus keys
        self.map_allowed_bonus_types = {
            globals.BONUS_SPEED: True,
            globals.BONUS_POWER: True,
            globals.BONUS_CAPACITY: True,
            globals.BONUS_LIFE: True,
            globals.BONUS_SLOWDOWN: True,
            globals.BONUS_REVERSE: True,
        }

    def collect(self, bonus):
        from entitites.bot import Bot

        if bonus.collector_key:
            return
        # Now we ensure that bonus is not collected by someone

        not_activated_bonus_cnt = 0
        for b_key in self.bonus_keys:
            b = globals.map_key_sprite[b_key]
            if not b.activated:
                not_activated_bonus_cnt += 1

        if not_activated_bonus_cnt >= 10:
            return

        self.bonus_keys.append(bonus.key)
        bonus.collector_key = self.key
        bonus.hidden = True
        bonus.ignore_collision = True

        if isinstance(self, Bot):
            bonus.activate()

    def activate_bonus_at(self, idx=0):  # NOTE: CANNOT receive negative index
        needed_idx = 0
        x = 0
        for i, b_key in enumerate(self.bonus_keys):  # ignoring activated bonuses and iterating over them
            b = globals.map_key_sprite[b_key]
            if b.activated:
                continue
            if x == idx:
                needed_idx = i
                break
            x += 1

        if needed_idx >= len(self.bonus_keys):
            return

        bonus = globals.map_key_sprite[self.bonus_keys[needed_idx]]
        bonus.activate()

    def get_bonus_instances(self):
        return list(map(lambda b_key: globals.map_key_sprite[b_key], self.bonus_keys))
