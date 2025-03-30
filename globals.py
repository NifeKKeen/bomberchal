import math
import utils.helpers

from collections import deque
from pygame.locals import K_a, K_d, K_w, K_s, K_LEFT, K_RIGHT, K_UP, K_DOWN
from config import load_controls
from entitites.bots.aggressive_bot import AGGRESSIVE_BOT_KEY
from entitites.bots.boss_bot import BOSS_BOT_KEY
from entitites.bots.original_bot import ORIGINAL_BOT_KEY
from entitites.bots.wandering_bot import WANDERING_BOT_KEY
from entitites.obstacle import MAP_SEED_OBSTACLE_KEY
from entitites.player import PLAYER_KEY

# region PYGAME VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
DISPLAYSURF = None  # pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
Frame = None  # pygame.time.Clock()
FPS = 60
all_sprites = None  # pygame.sprite.LayeredUpdates()
tick = 0  # whole app's tick
APP_VERSION = "1.1"
# endregion

# region FOR PAINT RENDER API
to_render_keys = set()
map_key_sprite = dict()
# endregion

# region ASSETS
SOUND_PATH = "assets/sound/"
MENU_MUSIC_PATH = "assets/sound/menu3.mp3"
MAP_GAMEMODE_MUSIC = {
    "pve": ["assets/sound/BG.mpeg", .1],
    "bossfight": ["assets/sound/BFG Division 2020.mp3", .4],
    "duel": ["assets/sound/BFG Division 2020.mp3", .4],
}
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
bonus_frames = [
    f"assets/images/bonus/{bonus_type}.png"
    for bonus_type in ["bomb_bonus", "explosion", "health", "speed", "slowdown", "reverse"]
]
# endregion

# region LAYOUT CONSTRAINTS
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
# endregion

# region MIXER VARIABLES
music_muted = True
sound_muted = False
current_music = None  # currently playing music name (as relative path to a file)
# endregion

# region FONT
FONT_PARAMETER = (None, 36)
TEXT_FONT = "assets/font/Pixeloid_Sans.ttf"
# endregion

# region NAVIGATION
current_page = "menu"
switched_page = False  # can change in current frame
switched_page_this_frame = True  # will be updated when frame ends
# endregion

# region EVENTS
frame_event_code_pairs = set()  # {(event_type, event_code)}
frame_unicodes = set()  # # {(event_type, event_unicode)}
frame_event_types = set()  # {event_type}
frame_keys_map = None  # pygame.get_pressed()
frame_keys = []  # list of currently pressed keys
# endregion

# region GAME STATES
cols = 21
rows = 21
field = None
field_fire_state = None  # power of fire in specific cell in ticks
field_free_state = None  # True if cell is free (empty or bonus), else False
field_weight = None  # weights of cells
paused = False
game_mode = None
scores = dict()
game_tick = 0  # current game's tick
inf = 1e9  # formal infinity used in field_weight and pathfinding in general

time_reversing_count_down = 0  # the number of ticks to do time reversing
time_slowdown_count_down = 0  # the number of ticks to run time slowly

SNAPSHOT_ALLOWED = True
SNAPSHOT_CAPTURE_DELAY = 15  # delay in ticks
state_snapshots = deque()
STATE_SNAPSHOTS_LIMIT = 4 * math.ceil(FPS / SNAPSHOT_CAPTURE_DELAY)  # events from last 4 seconds
cur_state_killed_sprites = set()
cur_state_spawned_sprites = set()

entities = set()
INITIAL_ORIGINAL_BOTS = 5
INITIAL_WANDERING_BOTS = 5
INITIAL_AGGRESSIVE_BOTS = 5
INITIAL_BOSS_BOTS = 0
INITIAL_BOXES = 50
INITIAL_BRICKS = 30
INITIAL_BONUS_SPAWN_DELAY = 400
# endregion

# region GAME CONSTRAINTS
CELL_SIZE = 32
PLAYER_CELL_SIZE = 28
VOID_CELL = 0
U_OBSTACLE_CELL = 1  # undestroyable obstacle
D_OBSTACLE_CELL = 2  # destroyable obstacle
ORIGINAL_BOT_CELL = 3  # starting cell for original bot
WANDERING_BOT_CELL = 4  # starting cell for wandering bot
AGGRESSIVE_BOT_CELL = 5  # starting cell for aggressive bot
BOSS_BOT_CELL = 6  # starting cell for boss bot
BONUS_SPEED = "speed"
BONUS_POWER = "power"
BONUS_CAPACITY = "capacity"
BONUS_LIFE = "life"
BONUS_SLOWDOWN = "slow"
BONUS_REVERSE = "reverse"
# endregion

# region TEXTURE TYPES
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
    BONUS_SPEED: bonus_frames[3],
    BONUS_POWER: bonus_frames[1],
    BONUS_CAPACITY: bonus_frames[0],
    BONUS_LIFE: bonus_frames[2],
    BONUS_SLOWDOWN: bonus_frames[4],
    BONUS_REVERSE: bonus_frames[5],
}
# endregion

# region OBJECT PROPERTIES
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
    BONUS_SPEED: utils.helpers.get_tick_from_ms(5000),
    BONUS_SLOWDOWN: utils.helpers.get_tick_from_ms(8000),
    BONUS_REVERSE: utils.helpers.get_tick_from_ms(7000),
}
# endregion

# region SCORING
scoring = {  # NOTE: for game_mode="dual" this variable is meaningless
    "KILL": {
        BOSS_BOT_KEY: 10000,
        AGGRESSIVE_BOT_KEY: 200,
        ORIGINAL_BOT_KEY: 100,
        WANDERING_BOT_KEY: 100,
        MAP_SEED_OBSTACLE_KEY[1]: 10,
        MAP_SEED_OBSTACLE_KEY[2]: 20,
    },
    "USE": {
        BONUS_SPEED: 10,
        BONUS_POWER: 10,
        BONUS_CAPACITY: 5,
        BONUS_LIFE: 10,
        BONUS_SLOWDOWN: 10,
        BONUS_REVERSE: 10,
    },
    "DAMAGE": {
        BOSS_BOT_KEY: 100,
        AGGRESSIVE_BOT_KEY: 20,
        ORIGINAL_BOT_KEY: 10,
        WANDERING_BOT_KEY: 10,
        MAP_SEED_OBSTACLE_KEY[1]: 3,
        MAP_SEED_OBSTACLE_KEY[2]: 3,
        PLAYER_KEY: -20,  # assuming the game mode is pve
    },
    "SELF_DAMAGE": -20,
    "SELF_KILL": -100,
}
# endregion

# region MOVE DIRECTIONS
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
# endregion

# region CUSTOM SETTINGS VARIABLES
MAX_USERNAME_LENGTH = 15
usernames = ["", ""]

setup_data = {
    "ranges":
        [  # label, texture_path, value, left_arrow sprite, value_text sprite, right_arrow sprite, step]
            ["Boxes", map_obstacle_type_to_path[OBSTACLE_CELL_BOX1], INITIAL_BOXES, None, None, None, 10],
            ["Bricks", map_obstacle_type_to_path[OBSTACLE_CELL_BRICKS], INITIAL_BRICKS, None, None, None, 10],
            ["Bonuse delay", bonus_frames[0], INITIAL_BONUS_SPAWN_DELAY, None, None, None, 20],
            ["Original bots", bot_frames["original"]["down_static"][0], INITIAL_ORIGINAL_BOTS, None, None, None, 1],
            ["Aggressive bots", bot_frames["aggressive"]["down_static"][0], INITIAL_AGGRESSIVE_BOTS, None, None, None,
             1],
            ["Wandering bots", bot_frames["wandering"]["down_static"][0], INITIAL_WANDERING_BOTS, None, None, None, 1],
            ["Rows", None, rows, None, None, None, 1],
            ["Cols", None, cols, None, None, None, 1],
            ["Lives", None, 1, None, None, None, 1],
        ],
    "players": 1,
    "index": {
        "boxes": 0,
        "bricks": 1,
        "bonus_delay": 2,
        "original_bots": 3,
        "aggressive_bots": 4,
        "wandering_bots": 5,
        "rows": 6,
        "cols": 7,
        "lives": 8,
    },
    "version": APP_VERSION,
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
    },
]

skins = {
    "ch1": "assets/images/characters/ch1/down.png",
    "ch2": "assets/images/characters/ch2/down.png",
    "ch3": "assets/images/characters/ch3/down.png",
    "ch4": "assets/images/characters/ch4/down.png",
}

skin_p1_id = 1
skin_p2_id = 2
# endregion
