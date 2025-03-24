import globals
from entitites.interfaces.Snapshotable import Snapshotable


class StateSnapshot:
    def __init__(self, sprites):
        self.map_key_to_sprite_snapshot = {}
        self.map_key_to_sprite_original = {}
        for sprite in sprites:
            if isinstance(sprite, Snapshotable):
                sprite_snapshot = sprite.get_snapshot()
                self.map_key_to_sprite_snapshot[sprite.key] = sprite_snapshot
                self.map_key_to_sprite_original[sprite.key] = sprite
