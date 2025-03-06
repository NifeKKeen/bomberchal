from collections import deque
from pygame.locals import K_a, K_d, K_w, K_s, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN  # необходимые ключи

# PYGAME VARIABLE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAYSURF = None  # pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
Frame = None #  pygame.time.Clock()
FPS = 60
FONT_PARAMETER = (None, 36)
menu_background_img = None
settings_background_img = None
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2
text_font = "assets/font/Pixeloid_Sans.ttf"
all_sprites = None #  pygame.sprite.LayeredUpdates()

# NAVIGATION
current_page = "menu"
switched_page = False  # can change in current frame
switched_page_this_frame = True # will be updated when frame ends


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

EXPLOSION_KEY_DEFAULT1 = K_SPACE
EXPLOSION_KEY_DEFAULT2 = K_RETURN
controls_players = [
    {
        "to_left_key": K_a,
        "to_right_key": K_d,
        "to_up_key": K_w,
        "to_down_key": K_s,
        "explosion_key": EXPLOSION_KEY_DEFAULT1
    },
    {
        "to_left_key": K_LEFT,
        "to_right_key": K_RIGHT,
        "to_up_key": K_UP,
        "to_down_key": K_DOWN,
        "explosion_key": EXPLOSION_KEY_DEFAULT2
    }
]
