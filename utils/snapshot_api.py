import globals
from entitites.StateSnapshot import StateSnapshot


def capture():
    if not globals.SNAPSHOT_ALLOWED:
        return

    snapshot_state = StateSnapshot(globals.all_sprites)

    globals.state_snapshots.append(snapshot_state)
    if len(globals.state_snapshots) > globals.STATE_SNAPSHOTS_LIMIT:
        globals.state_snapshots.popleft()


def restore_last_snapshot():
    if len(globals.state_snapshots) == 0:
        return

    last_state_snapshot = globals.state_snapshots.pop()
    last_state_snapshot.killed_sprites.update(globals.cur_state_killed_sprites)
    last_state_snapshot.spawned_sprites.update(globals.cur_state_spawned_sprites)

    globals.__dict__.update(last_state_snapshot.globals_snapshot)

    # ---------- current state events ------------
    for to_kill_sprite_key in last_state_snapshot.spawned_sprites:
        # we will fully remove the spawned entity in the last frame
        to_kill_sprite = globals.map_key_sprite[to_kill_sprite_key]
        to_kill_sprite.kill(True)
        # print("WILL DIE", to_kill_sprite_key)

    for to_spawn_sprite_key in last_state_snapshot.killed_sprites:
        if to_spawn_sprite_key in last_state_snapshot.spawned_sprites:
            # we will not restore sprites that were spawned and killed in the same frame
            continue
        # print("WILL LIVE", to_spawn_sprite_key)
        to_spawn_sprite = globals.map_key_sprite[to_spawn_sprite_key]
        to_spawn_sprite.restore_from_snapshot(to_spawn_sprite.last_snapshot)
        to_spawn_sprite.snapshotted = False
    # ---------- end of current state events ----------

    # ---------- last state events ------------
    for key, original_sprite in \
            last_state_snapshot.map_key_to_sprite_original.items():
        if original_sprite._removed:
            continue
        if key in last_state_snapshot.killed_sprites:
            # we already restored them
            continue

        sprite_snapshot = last_state_snapshot.map_key_to_sprite_snapshot[key]

        original_sprite.restore_from_snapshot(sprite_snapshot)
        original_sprite.snapshotted = False
        original_sprite.should_refresh = True
    # ---------- end of last state events ------------

    # print("SPAWNED", *map(lambda x: x, last_state_snapshot.spawned_sprites))
    # print("KILLED", *map(lambda x: x, last_state_snapshot.killed_sprites))

    globals.cur_state_killed_sprites.clear()
    globals.cur_state_spawned_sprites.clear()


def spawn_happened(sprite):
    if globals.cur_state_spawned_sprites is None:
        return
    else:
        globals.cur_state_spawned_sprites.add(sprite.key)


def kill_happened(sprite):
    if globals.cur_state_killed_sprites is None:
        sprite.kill(True)
    else:
        globals.cur_state_killed_sprites.add(sprite.key)
