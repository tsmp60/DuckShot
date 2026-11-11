"""Bankruptcy screen: shown when money <= 0. Replay or back to the menu."""
import pygame

from config import settings
from ui import Button, draw_text, make_overlay


class BankruptcyScreen:
    def __init__(self, manager):
        self.m = manager
        cx = settings.WIDTH // 2
        self.replay_btn = Button("Replay", (cx, 360))
        self.menu_btn = Button("Main Menu", (cx, 430))
        self.overlay = make_overlay(190)
        self.age = 0

    def on_enter(self):
        self.age = 0

    def on_exit(self):
        pass

    def _ready(self):
        # Short delay so frantic shooting clicks can't hit a button by accident
        return self.age >= settings.BUTTON_INPUT_DELAY

    def handle_event(self, event):
        if not self._ready():
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
                self.m.start_new_session()
            elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                self.m.go_to_menu()
        elif self.replay_btn.clicked(event):
            self.m.start_new_session()
        elif self.menu_btn.clicked(event):
            self.m.go_to_menu()

    def update(self):
        self.age += 1

    def draw(self, surface):
        # Frozen last frame of the game underneath
        if self.m.snapshot:
            surface.blit(self.m.snapshot, (0, 0))
        else:
            surface.fill((40, 40, 40))
        surface.blit(self.overlay, (0, 0))

        cx = settings.WIDTH // 2
        fonts = self.m.fonts
        draw_text(surface, fonts, "BANKRUPT", 110, settings.ALERT_COLOR, (cx, 190), "center")
        n = self.m.game.ducks_shot
        draw_text(
            surface, fonts, f"You shot {n} duck{'s' if n != 1 else ''}", 30,
            settings.TEXT_COLOR, (cx, 275), "center",
        )

        self.replay_btn.draw(surface, fonts)
        self.menu_btn.draw(surface, fonts)
        draw_text(
            surface, fonts, "ENTER: replay   |   M: main menu", 22,
            settings.MUTED_COLOR, (cx, settings.HEIGHT - 40), "center",
        )
