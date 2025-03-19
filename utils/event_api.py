import globals


def is_fired(event_type, event_code = None):
    if event_code is None:
        return event_type in globals.frame_event_types
    if event_code is not None:
        return (event_type, event_code) in globals.frame_event_code_pairs
    return False
