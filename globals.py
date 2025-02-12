from collections import deque

import pygame

# PYGAME VARIABLE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAYSURF = None  # pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
Frame = None #  pygame.time.Clock()
FPS = 60

all_sprites = None #  pygame.sprite.LayeredUpdates()

# NAVIGATION
current_page = "menu"
switched_page = False

# EVENTS
frame_events = set()

# FOR PAINT RENDER API
to_render_keys = set()
map_key_sprite = dict()

cell_size = 32

# GAME STATES
field = None
paused = False
game_mode = None
scores = dict()
tick = 0
events_stack = deque()

entities = []
