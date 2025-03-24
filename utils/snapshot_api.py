import globals
from entitites.StateSnapshot import StateSnapshot


def capture():
    snapshot_state = StateSnapshot(globals.all_sprites)

    globals.state_snapshots.append(snapshot_state)
    if len(globals.state_snapshots) > globals.state_snapshots_limit:
        globals.state_snapshots.popleft()

def restore_last_snapshot():
    if len(globals.state_snapshots) == 0:
        return

    state_snapshot = globals.state_snapshots.pop()
    for key, original_sprite in state_snapshot.map_key_to_sprite_original.items():
        sprite_snapshot = state_snapshot.map_key_to_sprite_snapshot[original_sprite.key]
        original_sprite.restore_from_snapshot(sprite_snapshot)
        original_sprite.should_refresh = True
    print("SUCCESS")
