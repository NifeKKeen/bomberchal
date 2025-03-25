from copy import deepcopy, copy

import globals


class StateSnapshot:  # class with side effects!
    def __init__(self, sprites):
        if not globals.SNAPSHOT_ALLOWED:
            return

        from entitites.interfaces.Snapshotable import Snapshotable

        self.globals_snapshot = deepcopy(
            {
                key: getattr(globals, key)
                for key in ["field_fire_state", "field", "game_tick", "scores"]
            }
        )
        self.globals_snapshot["entities"] = copy(globals.entities)

        self.map_key_to_sprite_snapshot = {}
        self.map_key_to_sprite_original = {}
        self.killed_sprites = globals.cur_state_killed_sprites
        self.spawned_sprites = globals.cur_state_spawned_sprites

        globals.cur_state_killed_sprites = set()
        globals.cur_state_spawned_sprites = set()

        for sprite in sprites:
            if isinstance(sprite, Snapshotable):
                if sprite.snapshotted:
                    sprite_snapshot = sprite.last_snapshot
                else:
                    sprite_snapshot = sprite.get_snapshot()

                self.map_key_to_sprite_snapshot[sprite.key] = sprite_snapshot
                self.map_key_to_sprite_original[sprite.key] = sprite
                sprite.snapshotted = False
