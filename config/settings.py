"""All tweakable game constants live here."""
import os
import sys

# --- Platform -------------------------------------------------------------
IS_WEB = sys.platform == "emscripten"  # True when running in the browser (Pygbag)

# --- Paths ----------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

# --- Window ---------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
TITLE = "Duckshot"
CAPTION = "Duckshot - Riverbank Defense"
TAGLINE = "Shoot ducks. Earn money. Don't go broke."

# --- Colors (minimalist palette) -----------------------------------------
WHITE = (255, 255, 255)
TEXT_COLOR = (240, 240, 240)
MUTED_COLOR = (170, 170, 170)
GOLD_COLOR = (255, 215, 0)
ALERT_COLOR = (255, 90, 90)
PELLET_COLOR = (255, 255, 200)
DARK = (20, 20, 20)
OVERLAY_ALPHA = 170  # darkness of the menu / bankruptcy overlay (0-255)

# --- Economy --------------------------------------------------------------
START_MONEY = 100
RELOAD_COST = 10
ESCAPE_PENALTY = 20  # money lost when a duck gets past you

# --- Weapon ---------------------------------------------------------------
PLAYER_POS = (670, 480)
AMMO_MAX = 6
RELOAD_FRAMES = 35
PELLETS_PER_SHOT = 7
PELLET_SPREAD = 0.16
PELLET_SPEED = (16, 22)
PELLET_LIFE = 32
MUZZLE_OFFSET = 34

# --- Ducks ----------------------------------------------------------------
SPAWN_INTERVAL = 65  # frames between spawns
SPAWN_X_RANGE = (230, 570)
DUCK_TYPES = {
    "mallard": {"speed": (2.0, 3.2), "reward": 15, "radius": 20, "height": 50},
    "yellow": {"speed": (3.8, 5.2), "reward": 25, "radius": 16, "height": 44},
}

# --- UI -------------------------------------------------------------------
BUTTON_SIZE = (240, 52)
BUTTON_INPUT_DELAY = 40  # frames after a screen opens before buttons react
