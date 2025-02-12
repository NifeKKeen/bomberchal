from pygame.locals import *
import globals

def is_fired(event_type):
    return event_type in globals.frame_events
