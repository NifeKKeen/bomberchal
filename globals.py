from collections import deque
from pygame.locals import K_a, K_d, K_w, K_s, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN  # необходимые ключи
from config import load_config
import utils.helpers

# PYGAME VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
DISPLAYSURF = None  # pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
Frame = None  # pygame.time.Clock()
FPS = 60
all_sprites = None  # pygame.sprite.LayeredUpdates()

# FOR PAINT RENDER API
to_render_keys = set()
map_key_sprite = dict()

# ASSETS
SOUND_PATH = "assets/sound/"
MENU_MUSIC_PATH = "assets/sound/menu3.mp3"
GAME_MUSIC_PATH1 = "assets/sound/BG.mpeg"
GAME_MUSIC_PATH2 = "assets/sound/BFG Division 2020.mp3"
EXPLOSION_SOUND_PATH = "assets/sound/explosion1.mp3"

menu_background_img = None
brown_background_img = None
MUTED_IMG_PATH1 = "assets/images/mute/mute.png"
UNMUTED_IMG_PATH1 = "assets/images/mute/volume.png"
MUTED_IMG_PATH2 = "assets/images/mute/mute2.png"
UNMUTED_IMG_PATH2 = "assets/images/mute/volume2.png"

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
    } for bot_type in ["original", "wandering", "aggressive", "boss"]
}

explosion_frames = [f"assets/images/explosion/{i}.png" for i in range(3, 0, -1)]
bomb_frames = [f"assets/images/bomb/{i}.png" for i in range(1, 4)]
box_frames = [f"assets/images/terrain/box{i}.png" for i in range(1, 3)]
bricks_frames = [f"assets/images/terrain/wall1.png"]
bricks_crack_frames = [f"assets/images/terrain/wall_crack{i}.png" for i in range(1, 3)]
border_frames = [f"assets/images/terrain/block{i}.png" for i in range(1, 3)]
grass_frames = ["assets/images/terrain/grass1.png"]
bonus_frames = ["assets/images/bonus/bomb_bonus.png", "assets/images/bonus/explosion.png", "assets/images/bonus/health.png"]

# LAYOUT CONSTRAINTS
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
SHADOW_OFFSET = 4
SHADOW_COLOR = (64, 64, 64)

BUTTON_LAYER = 10
TEXT_LAYER = 60
SHADOW_LAYER = 59
LAYER_SHIFT = 100  # for popups
BASE_ENTITY_LAYER = 10
BASE_OBSTACLE_LAYER = 20

# MIXER VARIABLES
music_muted = True
sound_muted = False
current_music = None  # currently playing music name (as relative path to a file)

# FONT
FONT_PARAMETER = (None, 36)
TEXT_FONT = "assets/font/Pixeloid_Sans.ttf"

# NAVIGATION
current_page = "menu"
switched_page = False  # can change in current frame
switched_page_this_frame = True # will be updated when frame ends

# EVENTS
frame_event_code_pairs = set()  # {(event_type, event_code)}
frame_event_types = set()  # {event_type}
frame_keys_map = None  # pygame.get_pressed()
frame_keys = []  # list of currently pressed keys

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
initial_bots_count = [10, 10, 10, 0]  # original, wandering, aggressive, boss
initial_obstacle_count = 0

# GAME CONSTRAINTS
CELL_SIZE = 32
PLAYER_CELL_SIZE = 28
VOID_CELL = 0
U_OBSTACLE_CELL = 1  # undestroyable obstacle
D_OBSTACLE_CELL = 2  # destroyable obstacle
ORIGINAL_BOT_CELL = 3  # starting cell for original bot
WANDERING_BOT_CELL = 4  # starting cell for wandering bot
AGGRESSIVE_BOT_CELL = 5  # starting cell for aggressive bot
BOSS_BOT_CELL = 6  # starting cell for boss bot
BONUS_SPEED = "Speed"
BONUS_POWER = "Power"
BONUS_CAPACITY = "Capacity"
BONUS_LIFE = "Life"

# TEXTURE TYPES
OBSTACLE_CELL_BORDER1 = 10
OBSTACLE_CELL_BORDER2 = 11
OBSTACLE_CELL_BOX1 = 12
OBSTACLE_CELL_BOX2 = 13
OBSTACLE_CELL_BRICKS = 14
OBSTACLE_CELL_BRICKS_STATE1 = 15
OBSTACLE_CELL_BRICKS_STATE2 = 16
map_obstacle_type_to_path = {
    OBSTACLE_CELL_BORDER1: border_frames[0],
    OBSTACLE_CELL_BORDER2: border_frames[1],
    OBSTACLE_CELL_BOX1: box_frames[0],
    OBSTACLE_CELL_BOX2: box_frames[1],
    OBSTACLE_CELL_BRICKS: bricks_frames[0],
    OBSTACLE_CELL_BRICKS_STATE1: bricks_crack_frames[0],
    OBSTACLE_CELL_BRICKS_STATE2: bricks_crack_frames[1],
}
map_bonus_type_to_path = {
    BONUS_SPEED: None ,
    BONUS_POWER: bonus_frames[1],
    BONUS_CAPACITY: bonus_frames[0],
    BONUS_LIFE: bonus_frames[2],
}

# OBJECT PROPERTIES
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
map_bonus_type_to_timer = {
    BONUS_LIFE: float('inf'),
    BONUS_POWER: utils.helpers.get_tick_from_ms(10000),
    BONUS_CAPACITY: utils.helpers.get_tick_from_ms(30000),
    BONUS_SPEED: utils.helpers.get_tick_from_ms(50000),
}

# MOVE DIRECTIONS
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

# CUSTOM SETTINGS VARIABLES
exp_key_p1 = K_SPACE
exp_key_p2 = K_RETURN
load_config()

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
    "ch1": "assets/images/characters/ch1/down.png",
    "ch2": "assets/images/characters/ch2/down.png",
    "ch3": "assets/images/characters/ch3/down.png",
    "ch4": "assets/images/characters/ch4/down.png"
}

skin_p1_id = 1
skin_p2_id = 2