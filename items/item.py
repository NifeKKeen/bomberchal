class Item:
    def __init__(self, **kwargs):
        self.is_infinite = kwargs.get("is_infinite", False)
        self.count = kwargs.get("count", 0)
        self.timer = kwargs.get("timer", float('inf'))
