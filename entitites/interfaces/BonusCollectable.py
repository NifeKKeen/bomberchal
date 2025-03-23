from entitites.entity import Entity


class BonusCollectable(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bonuses = kwargs.get("bonuses", [])  # Bonus instances

    def collect(self, bonus):
        from entitites.bot import Bot

        if bonus.collector:
            return
        # Now we ensure that bonus is not collected by someone

        not_activated_bonus_cnt = 0
        for b in self.bonuses:
            if not b.activated:
                not_activated_bonus_cnt += 1

        if not_activated_bonus_cnt >= 10:
            return

        self.bonuses.append(bonus)
        bonus.collector = self
        bonus.hidden = True
        bonus.ignore_collision = True

        if isinstance(self, Bot):
            bonus.activate()

    def activate_bonus_at(self, idx = 0):  # NOTE: CANNOT receive negative index
        needed_idx = 0
        x = 0
        for i, b in enumerate(self.bonuses):  # ignoring activated bonuses and iterating over them
            if self.bonuses[i].activated:
                continue
            if x == idx:
                needed_idx = i
                break
            x += 1

        if needed_idx >= len(self.bonuses):
            return

        self.bonuses[needed_idx].activate()
