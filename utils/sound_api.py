from os import path
import globals, pygame
from utils.helpers import rand


def play_music(music_path, volume = 1, override = False, ignore_mute = False):
    if not ignore_mute and globals.music_muted:
        return

    if override or globals.current_music != music_path:
        globals.current_music = music_path
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

def stop_music():
    globals.current_music = None
    pygame.mixer.music.stop()

def play_sound(sound_path, volume = 1, ignore_mute = False):
    if not ignore_mute and globals.sound_muted:
        return

    sound = pygame.mixer.Sound(sound_path)
    sound.set_volume(volume)
    sound.play()

def play_menu_music(randomly = True, index = None, volume = 1, ignore_mute = False):
    if not ignore_mute and globals.music_muted:
        return

    play_music(globals.MENU_MUSIC_PATH, volume=volume)

def play_explosion_sound(randomly = True, index = None, volume = 1, ignore_mute = False):
    if not ignore_mute and globals.sound_muted:
        return

    if randomly or index is None:
        index = rand(1, 5)
    play_sound(path.join(globals.SOUND_PATH, f"Explosion{index}.ogg"), volume)
