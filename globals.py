import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAYSURF = None  # pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
current_page = "menu"
switched_page = False

Frame = None #  pygame.time.Clock()
FPS = 60
all_sprites = None #  pygame.sprite.LayeredUpdates()

frame_events = []

# FOR PAINT RENDER API

to_render_keys = set()
map_key_sprite = dict()
