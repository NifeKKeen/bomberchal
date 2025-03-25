from typing import Protocol

import globals
from copy import deepcopy
from utils.paint_api import SurfaceSprite


class SnapshotableProtocol(Protocol):
    key: str | None
    mounted: bool
    mount: lambda: SurfaceSprite


class Snapshotable(SnapshotableProtocol):
    snapshotted = False
    last_snapshot = None  # copy of an object before it is killed

    def get_snapshot(self):
        if not globals.SNAPSHOT_ALLOWED:
            return None

        snapshot = {}
        for key, value in self.__dict__.items():
            if key not in ("image", "_Sprite__g", "last_snapshot", "kwargs"):
                # print(self.key, key, value)
                snapshot[key] = deepcopy(value)
        self.snapshotted = True
        return snapshot

    def try_snapshot(self):
        if globals.SNAPSHOT_ALLOWED and not self.snapshotted:
            self.snapshotted = True
            self.last_snapshot = self.get_snapshot()

    def restore_from_snapshot(self, snapshot):
        if snapshot is None:
            return

        self.__dict__.update(snapshot)
        if self.mounted:
            self.mount()
        globals.entities.add(self)
