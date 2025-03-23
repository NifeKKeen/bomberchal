import os, pygame, configparser, globals

CONFIG_FILE = "pages/menu/config.ini"

def parse_key(key_str, default_key):

    key_str = key_str.strip().lower()
    if key_str == "custom":
        return "custom"
    try:
        return int(key_str)  
    except ValueError:
        try:
            return pygame.key.key_code(key_str)  
        except Exception:
            return default_key  

def load_config():
    if not os.path.exists(CONFIG_FILE):
        globals.skin_p1_id = 1
        globals.skin_p2_id = 2
        globals.game_mode = "default"
        globals.explosion_key_p1 = pygame.K_SPACE
        globals.explosion_key_p2 = pygame.K_RETURN
        return
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    key1_str = config.get("Controls", "explosion_key_p1", fallback="space")
    key2_str = config.get("Controls", "explosion_key_p2", fallback="return")
    globals.explosion_key_p1 = parse_key(key1_str, pygame.K_SPACE)
    globals.explosion_key_p2 = parse_key(key2_str, pygame.K_RETURN)
    
    if "Skin" in config:
        globals.skin_p1_id = config.getint("Skin", "skin_p1_id", fallback=1)
        globals.skin_p2_id = config.getint("Skin", "skin_p2_id", fallback=2)
    else:
        globals.skin_p1_id = 1
        globals.skin_p2_id = 2
    
    if "Game" in config:
        globals.game_mode = config.get("Game", "mode", fallback="default")
    else:
        globals.game_mode = "default"