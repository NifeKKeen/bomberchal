from pygame.locals import *
import globals

def is_fired(event_type, event_code):
    return (event_type, event_code) in globals.frame_events
