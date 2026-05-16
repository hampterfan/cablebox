import os

# Base project directory (the folder where config.py lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
MEDIA_PATH = "/mnt/media"  # USB drive mount
BG_IMAGE_PATH = os.path.join(BASE_DIR, "images", "bg.jpg")

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30

# Icons
ICON_WIDTH = 200
ICON_HEIGHT = 280

# Sounds
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
SCROLL_SOUND_PATH = os.path.join(SOUNDS_DIR, "hover.wav")
SCROLL_SOUND_VOLUME = 0.3
SELECT_SOUND_PATH = os.path.join(SOUNDS_DIR, "select.wav")
SELECT_SOUND_VOLUME = 0.3
CLOSE_SOUND_PATH = os.path.join(SOUNDS_DIR, "close.wav")
CLOSE_SOUND_VOLUME = 0.3
RANDOM_SOUND_PATH = os.path.join(SOUNDS_DIR, "random.wav")
RANDOM_SOUND_VOLUME = 0.3

# Video
ENTER_DEBOUNCE_MS = 100

# Encoders
ENCODER_CONFIG = {
    "Encoder1": {"a": 17, "b": 18, "btn": 27},
    "Encoder2": {"a": 22, "b": 23, "btn": 24},
    "Encoder3": {"a": 5, "b": 6, "btn": 12}
}
