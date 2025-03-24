from copy import deepcopy

import globals


class StateSnapshot:  # class with side effects!
    def __init__(self, sprites):
        from entitites.interfaces.Snapshotable import Snapshotable

        self.globals_snapshot = deepcopy(
            {
                key: getattr(globals, key)
                for key in ["field_fire_state", "field", "game_tick", "scores"]
            }
        )

        self.map_key_to_sprite_snapshot = {}
        self.map_key_to_sprite_original = {}
        self.killed_sprites = globals.cur_state_killed_sprites
        self.spawned_sprites = globals.cur_state_spawned_sprites

        globals.cur_state_killed_sprites = set()
        globals.cur_state_spawned_sprites = set()

        for sprite in sprites:
            if isinstance(sprite, Snapshotable):
                sprite_snapshot = sprite.get_snapshot()
                self.map_key_to_sprite_snapshot[sprite.key] = sprite_snapshot
                self.map_key_to_sprite_original[sprite.key] = sprite

    def clear(self):
        for sprite in self.killed_sprites:
            sprite.kill_from_memory()
        self.map_key_to_sprite_original.clear()
        self.map_key_to_sprite_snapshot.clear()
        self.killed_sprites.clear()
        self.spawned_sprites.clear()
