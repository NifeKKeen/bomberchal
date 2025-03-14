from collections import deque
from pygame.locals import K_a, K_d, K_w, K_s, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN  # необходимые ключи
from pages.menu.config import load_controls

# PYGAME VARIABLE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
DISPLAYSURF = None  # pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
Frame = None #  pygame.time.Clock()
FPS = 60

center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

current_music = None  # currently playing music name (as relative path to a file)
menu_music_path = "assets/sound/menu3.mp3"
game_music_path = "assets/sound/BG.mpeg"

menu_background_img = None
brown_background_img = None

FONT_PARAMETER = (None, 36)
text_font = "assets/font/Pixeloid_Sans.ttf"

all_sprites = None #  pygame.sprite.LayeredUpdates()
is_muted = False
# NAVIGATION
current_page = "menu"
switched_page = False  # can change in current frame
switched_page_this_frame = True # will be updated when frame ends


# EVENTS
frame_event_code_pairs = set()  # {(event_type, event_code)}
frame_event_types = set()  # {event_type}
frame_keys_map = None  # pygame.get_pressed()
frame_keys = []  # list of currently pressed keys

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
exp_key_p1, exp_key_p2 = load_controls()

controls_players = [
    {
        "to_left_key": K_a,
        "to_right_key": K_d,
        "to_up_key": K_w,
        "to_down_key": K_s,
        "explosion_key": exp_key_p1
    },
    {
        "to_left_key": K_LEFT,
        "to_right_key": K_RIGHT,
        "to_up_key": K_UP,
        "to_down_key": K_DOWN,
        "explosion_key": exp_key_p2
    }
]


skins = [
    {
        "ch1": "assets/characters/ch1/11.png",
        "ch2": "assets/characters/ch2/22.png",
        "ch3": "assets/characters/ch3/33.png",
        "ch4": "assets/characters/ch4/44.png"
    }
]


skins_gifs = [
    "assets/characters/ch1/11.gif",
    "assets/characters/ch2/22.gif",
    "assets/characters/ch3/33.gif",
    "assets/characters/ch4/44.gif"
]
player_skins = {
    "ch1": skins[0]["ch1"],
    "ch2": skins[0]["ch2"]
}