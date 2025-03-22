from collections import deque
from pygame.locals import K_a, K_d, K_w, K_s, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN  # необходимые ключи
from pages.menu.config import load_controls

# PYGAME VARIABLE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
DISPLAYSURF = None  # pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
Frame = None #  pygame.time.Clock()
FPS = 60

CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
SHADOW_OFFSET = 4
SHADOW_COLOR = (64, 64, 64)

music_muted = True
sound_muted = False
current_music = None  # currently playing music name (as relative path to a file)
sound_path = "assets/sound/"
menu_music_path = "assets/sound/menu3.mp3"
game_music_path = "assets/sound/BG.mpeg"
explosion_sound_path = "assets/sound/explosion1.mp3"

menu_background_img = None
brown_background_img = None
unmuted_img = "assets/images/mute/volume.png"
muted_img = "assets/images/mute/mute.png"

character_frames = {
    f"ch{chi}": {
        "top_static": [f"assets/images/characters/ch{chi}/up.png"],
        "top_moving": [f"assets/images/characters/ch{chi}/up{i}.png" for i in range(1, 3)],
        "right_static": [f"assets/images/characters/ch{chi}/right.png"],
        "right_moving": [f"assets/images/characters/ch{chi}/right{i}.png" for i in range(1, 3)],
        "down_static": [f"assets/images/characters/ch{chi}/down.png"],
        "down_moving": [f"assets/images/characters/ch{chi}/down{i}.png" for i in range(1, 3)],
        "left_static": [f"assets/images/characters/ch{chi}/left.png"],
        "left_moving": [f"assets/images/characters/ch{chi}/left{i}.png" for i in range(1, 3)]
    } for chi in range(1, 5)
}
bot_frames = {
    f"{bot_type}": {
        "top_static": [f"assets/images/bots/{bot_type}/up.png"],
        "top_moving": [f"assets/images/bots/{bot_type}/up{i}.png" for i in range(1, 3)],
        "right_static": [f"assets/images/bots/{bot_type}/right.png"],
        "right_moving": [f"assets/images/bots/{bot_type}/right{i}.png" for i in range(1, 3)],
        "down_static": [f"assets/images/bots/{bot_type}/down.png"],
        "down_moving": [f"assets/images/bots/{bot_type}/down{i}.png" for i in range(1, 3)],
        "left_static": [f"assets/images/bots/{bot_type}/left.png"],
        "left_moving": [f"assets/images/bots/{bot_type}/left{i}.png" for i in range(1, 3)]
    } for bot_type in ["wandering"]
}

explosion_frames = [f"assets/images/explosion/{i}.png" for i in range(3, 0, -1)]
bomb_frames = [f"assets/images/bomb/{i}.png" for i in range(1, 4)]
box_frames = [f"assets/images/terrain/box{i}.png" for i in range(1, 3)]
bricks_frames = [f"assets/images/terrain/wall1.png"]
bricks_crack_frames = [f"assets/images/terrain/wall_crack{i}.png" for i in range(1, 3)]
border_frames = [f"assets/images/terrain/block{i}.png" for i in range(1, 3)]
grass_frames = ["assets/images/terrain/grass1.png"]
bonus_frames = []

FONT_PARAMETER = (None, 36)
text_font = "assets/font/Pixeloid_Sans.ttf"

all_sprites = None #  pygame.sprite.LayeredUpdates()

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
game_mode = "default"
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
U_OBSTACLE_CELL = 1  # undestroyable obstacle
D_OBSTACLE_CELL = 2  # destroyable obstacle
BOT_CELL = 3  # starting cell for bot

# texture_types
OBSTACLE_CELL_BORDER1 = 10
OBSTACLE_CELL_BORDER2 = 11
OBSTACLE_CELL_BOX1 = 12
OBSTACLE_CELL_BOX2 = 13
OBSTACLE_CELL_BRICKS = 14
OBSTACLE_CELL_BRICKS_STATE1 = 15
OBSTACLE_CELL_BRICKS_STATE2 = 16
map_type_to_path = {
    OBSTACLE_CELL_BORDER1: border_frames[0],
    OBSTACLE_CELL_BORDER2: border_frames[1],
    OBSTACLE_CELL_BOX1: box_frames[0],
    OBSTACLE_CELL_BOX2: box_frames[1],
    OBSTACLE_CELL_BRICKS: bricks_frames[0],
    OBSTACLE_CELL_BRICKS_STATE1: bricks_crack_frames[0],
    OBSTACLE_CELL_BRICKS_STATE2: bricks_crack_frames[1],
}

# obstacle properties
map_obstacle_seed_to_props = {
    0: {
        "stage_texture_types": [
            [OBSTACLE_CELL_BORDER1],
            [OBSTACLE_CELL_BORDER2],
        ],
        "lives": float('inf'),
    },
    1: {
        "stage_texture_types": [
            [OBSTACLE_CELL_BOX1],
            [OBSTACLE_CELL_BOX2],
        ],
        "lives": 1,
    },
    2: {
        "stage_texture_types": [
            [OBSTACLE_CELL_BRICKS, OBSTACLE_CELL_BRICKS_STATE1, OBSTACLE_CELL_BRICKS_STATE2],
        ],
        "lives": 3,
    },
}

BFS_DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
UP_DIRECTION = (0, -1)
RIGHT_DIRECTION = (1, 0)
DOWN_DIRECTION = (0, 1)
LEFT_DIRECTION = (-1, 0)
MAP_DIRECTION = {
    "up": UP_DIRECTION,
    "right": RIGHT_DIRECTION,
    "down": DOWN_DIRECTION,
    "left": LEFT_DIRECTION,
}

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


skins = {
    "ch1": "assets/gifs/ch1/1.png",
    "ch2": "assets/gifs/ch2/1.png",
    "ch3": "assets/gifs/ch3/1.png",
    "ch4": "assets/gifs/ch4/1.png"
}

skin_p1_id = 1
skin_p2_id = 2