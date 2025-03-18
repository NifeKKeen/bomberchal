import pygame, configparser


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

def load_controls():
    config = configparser.ConfigParser()
    config.read("pages/menu/config.ini")

    key1_str = config.get("Controls", "explosion_key_p1", fallback="space")
    key2_str = config.get("Controls", "explosion_key_p2", fallback="m")

    key1 = parse_key(key1_str, pygame.K_SPACE)
    key2 = parse_key(key2_str, pygame.K_m)

    return key1, key2
