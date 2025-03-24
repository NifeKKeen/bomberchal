from copy import deepcopy, copy



class Snapshotable:
    def get_snapshot(self):
        snapshot = {}
        for key, value in self.__dict__.items():
            if key not in ("image", "_Sprite__g"):
                # print(self.key, key, value)
                if key in ("entity_group", "kwargs", "spawner", "collector"):
                    snapshot[key] = copy(value)
                elif key in ("bonuses"):
                    snapshot[key] = [copy(element) for element in value]
                else:
                    snapshot[key] = deepcopy(value)
        return snapshot

    def restore_from_snapshot(self, snapshot):
        self.__dict__.update(snapshot)
