from items.item import Item


class BonusItem(Item):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonus_id = kwargs.get("bonus_id", 0)
