import globals
from entitites.StateSnapshot import StateSnapshot


def capture():
    snapshot_state = StateSnapshot(globals.all_sprites)

    globals.state_snapshots.append(snapshot_state)
    if len(globals.state_snapshots) > globals.STATE_SNAPSHOTS_LIMIT:
        to_remove = globals.state_snapshots.popleft()
        to_remove.clear()

def restore_last_snapshot():
    if len(globals.state_snapshots) == 0:
        return

    last_state_snapshot = globals.state_snapshots.pop()
    globals.__dict__.update(last_state_snapshot.globals_snapshot)

    for to_kill_sprite in last_state_snapshot.spawned_sprites:
        to_kill_sprite.kill(True)  # we will fully remove the spawned entity in the last frame

    for to_spawn_sprite in last_state_snapshot.killed_sprites:
        if to_spawn_sprite in last_state_snapshot.spawned_sprites:  # we will not restore sprites that were spawned and killed in the same frame
            continue

        to_spawn_sprite.restore_from_snapshot(to_spawn_sprite.snapshot_before_kill)
        to_spawn_sprite.snapshot_before_kill = None

    for key, original_sprite in \
            last_state_snapshot.map_key_to_sprite_original.items():
        if original_sprite._removed:
            continue
        if original_sprite in last_state_snapshot.killed_sprites:
            continue

        sprite_snapshot = last_state_snapshot.map_key_to_sprite_snapshot[key]

        original_sprite.restore_from_snapshot(sprite_snapshot)
        original_sprite.should_refresh = True
    print("SUCCESS")

def spawn_happened(sprite):
    if globals.cur_state_spawned_sprites is None:
        return
    else:
        globals.cur_state_spawned_sprites.add(sprite)

def kill_happened(sprite):
    if globals.cur_state_killed_sprites is None:
        sprite.kill_from_memory()
    else:
        globals.cur_state_killed_sprites.add(sprite)
