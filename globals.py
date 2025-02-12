from collections import deque

# PYGAME VARIABLE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAYSURF = None  # pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
Frame = None #  pygame.time.Clock()
FPS = 60

all_sprites = None #  pygame.sprite.LayeredUpdates()

# NAVIGATION
current_page = "menu"
switched_page = False  # can change in current frame
switched_page_this_frame = False # will be updated when frame ends

# EVENTS
frame_events = set()  # {(event_type, event_code)}
frame_keys = None  # pygame.get_pressed()

# FOR PAINT RENDER API
to_render_keys = set()
map_key_sprite = dict()

cell_size = 32

# GAME STATES
cols = 0
rows = 0
field = None
paused = False
game_mode = None
scores = dict()
tick = 0
events_stack = deque()  # TODO
entities = set()

# GAME CONSTRAINTS
VOID_CELL = 0
U_OBSTACLE_CELL = 1  # TODO
