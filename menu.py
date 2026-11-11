"""Main menu screen: title, Play, Quit."""
import pygame

from config import settings
from ui import Button, draw_text, make_overlay


class MenuScreen:
    def __init__(self, manager):
        self.m = manager
        cx = settings.WIDTH // 2
        self.play_btn = Button("Play", (cx, 340))
        self.quit_btn = None if settings.IS_WEB else Button("Quit Game", (cx, 410))
        self.overlay = make_overlay()

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.m.start_new_session()
            elif event.key == pygame.K_ESCAPE and self.quit_btn:
                self.m.quit()
        elif self.play_btn.clicked(event):
            self.m.start_new_session()
        elif self.quit_btn and self.quit_btn.clicked(event):
            self.m.quit()

    def update(self):
        pass

    def draw(self, surface):
        bg = self.m.assets["bg"]
        if bg:
            surface.blit(bg, (0, 0))
        else:
            surface.fill((40, 40, 40))
        surface.blit(self.overlay, (0, 0))

        cx = settings.WIDTH // 2
        draw_text(surface, self.m.fonts, settings.TITLE.upper(), 120, settings.WHITE, (cx, 190), "center")
        draw_text(surface, self.m.fonts, settings.TAGLINE, 26, settings.GOLD_COLOR, (cx, 255), "center")

        self.play_btn.draw(surface, self.m.fonts)
        if self.quit_btn:
            self.quit_btn.draw(surface, self.m.fonts)

        draw_text(
            surface, self.m.fonts, "Click or press ENTER to play", 22,
            settings.MUTED_COLOR, (cx, settings.HEIGHT - 40), "center",
        )
