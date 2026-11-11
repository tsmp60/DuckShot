"""Loads images and fonts once, safely (missing files never crash the game)."""
import os

import pygame

from config import settings


def _load(name, alpha=True):
    path = os.path.join(settings.IMAGE_DIR, name)
    if not os.path.exists(path):
        return None
    img = pygame.image.load(path)
    return img.convert_alpha() if alpha else img.convert()


def _fit_height(surface, height):
    """Scale to a given height, keeping the aspect ratio."""
    w, h = surface.get_size()
    return pygame.transform.smoothscale(surface, (max(1, int(w * height / h)), height))


def _crop_to_content(surface):
    return surface.subsurface(surface.get_bounding_rect()).copy()


def load_assets():
    assets = {"bg": None, "player": None, "duck_mallard": None, "duck_yellow": None}

    bg = _load("river_bg_2.jpg", alpha=False)
    if bg:
        assets["bg"] = pygame.transform.smoothscale(bg, (settings.WIDTH, settings.HEIGHT))

    player = _load("player.png")
    if player:
        w, h = player.get_size()
        assets["player"] = pygame.transform.smoothscale(player, (88, int(88 * h / w)))

    sheet = _load("duckling_sheet.png")
    if sheet:
        sw, sh = sheet.get_size()
        top = _crop_to_content(sheet.subsurface(pygame.Rect(0, 0, sw, sh // 2)))
        bottom = _crop_to_content(sheet.subsurface(pygame.Rect(0, sh // 2, sw, sh - sh // 2)))
        assets["duck_mallard"] = _fit_height(top, settings.DUCK_TYPES["mallard"]["height"])
        assets["duck_yellow"] = _fit_height(bottom, settings.DUCK_TYPES["yellow"]["height"])

    return assets


class Fonts:
    """Caches fonts by size. Drop a .ttf in assets/fonts and set FONT_FILE to use it."""

    FONT_FILE = None  # e.g. "pixel.ttf"

    def __init__(self):
        self._cache = {}

    def get(self, size):
        if size not in self._cache:
            path = os.path.join(settings.FONT_DIR, self.FONT_FILE) if self.FONT_FILE else None
            if path and os.path.exists(path):
                self._cache[size] = pygame.font.Font(path, size)
            else:
                self._cache[size] = pygame.font.Font(None, size)  # built-in, works in browser
        return self._cache[size]
