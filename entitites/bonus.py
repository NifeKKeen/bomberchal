from entitites.entity import Entity

class Bonus(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bonus_id = kwargs.get("bonus_id", 0)
        self.timer = kwargs.get("timer", 0)
        self.type = kwargs.get("type", "Speed")
        # Speed - increases speed of collector by 2 times for 5 seconds
        # Power - increases power of collector's last bomb by 1
        # Capacity - increases capacity (bomb_allowed) of collector by 1
        self.collector = kwargs.get("collector", None)  # which entity collected bonus

    def collect(self, collector):
        self.collector = collector
        # print("Collected by ", self.collector)
        self.kill()

def bomb_types():
    return ["Speed", "Power", "Capacity"]