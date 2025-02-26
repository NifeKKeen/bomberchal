import globals
from entitites.entity import Entity

class Bonus(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonus_id = kwargs.get("bonus_id", 0)
        self.timer = kwargs.get("timer", 0)
        self.type = kwargs.get("type", 0)
        self.collector = kwargs.get("collector", None)  # which entity collected bonus

    def collect(self, **kwargs):
        self.collector = kwargs.get("collector", None)
        print("Collected by ", self.collector)
        self.unmount()
        globals.entities.remove(self)