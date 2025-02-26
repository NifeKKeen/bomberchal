from collections import deque

# PYGAME VARIABLE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
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

# GAME STATES
cols = 0
rows = 0
field = None
field_fire_state = None  # power of fire in specific cell in ticks
paused = False
game_mode = None
scores = dict()
tick = 0
events_stack = deque()  # TODO
entities = set()

# GAME CONSTRAINTS
cell_size = 32
player_cell_size = 28
VOID_CELL = 0
U_OBSTACLE_CELL = 1  # TODO
D_OBSTACLE_CELL = 2  # destroyable obstacle
BOT_CELL = 3  # starting cell for bot

directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]