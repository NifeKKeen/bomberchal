from copy import deepcopy, copy


class Snapshotable:
    def get_snapshot(self):
        snapshot = {}
        for key, value in self.__dict__.items():
            if key not in ("image", "_Sprite__g", "snapshot_before_kill"):
                # print(self.key, key, value)
                if key in ("entity_group", "kwargs"):
                    snapshot[key] = copy(value)
                else:
                    snapshot[key] = deepcopy(value)
        return snapshot

    def restore_from_snapshot(self, snapshot):
        if snapshot is None:
            return

        self.__dict__.update(snapshot)
        if self.mounted:
            self.mount()
        if self.entity_group:
            self.entity_group.add(self)
