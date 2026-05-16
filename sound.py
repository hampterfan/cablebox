# sound.py
import pygame
from config import SCROLL_SOUND_PATH, SCROLL_SOUND_VOLUME, SELECT_SOUND_PATH, SELECT_SOUND_VOLUME, CLOSE_SOUND_PATH, CLOSE_SOUND_VOLUME, RANDOM_SOUND_PATH, RANDOM_SOUND_VOLUME

def load_sounds():
    pygame.mixer.init()
    scroll_sound = pygame.mixer.Sound(SCROLL_SOUND_PATH)
    scroll_sound.set_volume(SCROLL_SOUND_VOLUME)

    select_sound = pygame.mixer.Sound(SELECT_SOUND_PATH)
    select_sound.set_volume(SELECT_SOUND_VOLUME)

    close_sound = pygame.mixer.Sound(CLOSE_SOUND_PATH)
    close_sound.set_volume(CLOSE_SOUND_VOLUME)

    random_sound = pygame.mixer.Sound(RANDOM_SOUND_PATH)
    random_sound.set_volume(RANDOM_SOUND_VOLUME)

    return scroll_sound, select_sound, close_sound, random_sound
