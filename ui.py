"""Small reusable UI pieces: text helpers, overlay and Button."""
import pygame

from config import settings


def draw_text(surface, fonts, text, size, color, pos, anchor="topleft", shadow=True):
    font = fonts.get(size)
    if shadow:
        sh = font.render(text, True, settings.DARK)
        surface.blit(sh, sh.get_rect(**{anchor: (pos[0] + 2, pos[1] + 2)}))
    img = font.render(text, True, color)
    rect = img.get_rect(**{anchor: pos})
    surface.blit(img, rect)
    return rect


def make_overlay(alpha=settings.OVERLAY_ALPHA):
    overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    return overlay


class Button:
    """Outlined minimalist button. Fills with gold on hover."""

    def __init__(self, label, center, size=settings.BUTTON_SIZE):
        self.label = label
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center

    def hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface, fonts):
        hover = self.hovered()
        if hover:
            pygame.draw.rect(surface, settings.GOLD_COLOR, self.rect, border_radius=8)
            color = settings.DARK
        else:
            pygame.draw.rect(surface, settings.WHITE, self.rect, width=2, border_radius=8)
            color = settings.WHITE
        draw_text(surface, fonts, self.label, 32, color, self.rect.center, "center", shadow=False)