import os
import configparser
import globals
import json
import pygame

from copy import copy
from utils.paint_api import SurfaceSprite


CONFIG_FILE = "config.ini"


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
    config.read(CONFIG_FILE)
    key1_str = config.get("Controls", "explosion_key_p1", fallback="space")
    key2_str = config.get("Controls", "explosion_key_p2", fallback="return")
 
    key1 = parse_key(key1_str, pygame.K_SPACE)
    key2 = parse_key(key2_str, pygame.K_RETURN)
 
    return key1, key2


def load_config():
    if not os.path.exists(CONFIG_FILE):
        globals.skin_p1_id = 1
        globals.skin_p2_id = 2
        globals.explosion_key_p1 = pygame.K_SPACE
        globals.explosion_key_p2 = pygame.K_RETURN
        globals.music_muted = False
        globals.sound_muted = False
        return
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if "Controls" in config:
        globals.explosion_key_p1 = parse_key(config.get("Controls", "explosion_key_p1", fallback="space"), pygame.K_SPACE)
        globals.explosion_key_p2 = parse_key(config.get("Controls", "explosion_key_p2", fallback="return"), pygame.K_RETURN)
    else:
        globals.explosion_key_p1 = pygame.K_SPACE
        globals.explosion_key_p2 = pygame.K_RETURN

    if "Skin" in config:
        globals.skin_p1_id = config.getint("Skin", "skin_p1_id", fallback=1)
        globals.skin_p2_id = config.getint("Skin", "skin_p2_id", fallback=2)
    else:
        globals.skin_p1_id = 1
        globals.skin_p2_id = 2

    if "Sound" in config:
        globals.music_muted = config.getboolean("Sound", "music", fallback=False)
        globals.sound_muted = config.getboolean("Sound", "sound", fallback=False)
    else:
        globals.music_muted = False
        globals.sound_muted = False

    if "Usernames" in config:
        globals.usernames = json.loads(config.get("Usernames", "usernames", fallback=globals.usernames))

    if "GameSetup" in config:
        globals.setup_data = json.loads(config.get("GameSetup", "setup_data", fallback=globals.setup_data))


def save_config():
    config = configparser.ConfigParser()
    config["Controls"] = {
        "explosion_key_p1": str(globals.controls_players[0]["explosion_key"]),
        "explosion_key_p2": str(globals.controls_players[1]["explosion_key"])
    }

    config["Sound"] = {
        "music": str(globals.music_muted).lower(),  # приводим к "true" или "false"
        "sound": str(globals.sound_muted).lower()
    }

    config["Usernames"] = {
        "usernames": str(json.dumps(globals.usernames))
    }

    config["GameSetup"] = {
        "setup_data": str(json.dumps(normalize_setup_data(globals.setup_data)))
    }

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def normalize_setup_data(setup_data):
    res = copy(setup_data)
    for i, data in enumerate(setup_data["ranges"]):
        res["ranges"][i] = list(map(lambda x: x if not isinstance(x, SurfaceSprite) else None, data))
    return res
