"""The actual game: ducks, shooting, reloading, money."""
import math
import random

import pygame

from config import settings
from ui import draw_text


class GameplayScreen:
    def __init__(self, manager):
        self.m = manager

    # --- lifecycle --------------------------------------------------------
    def on_enter(self):
        pygame.mouse.set_visible(False)  # we draw our own crosshair

    def on_exit(self):
        pygame.mouse.set_visible(True)

    # --- input ------------------------------------------------------------
    def handle_event(self, event):
        g = self.m.game
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.fire(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reload()
            elif event.key == pygame.K_ESCAPE:
                self.m.go_to_menu()

    def fire(self, target):
        g = self.m.game
        if g.ammo <= 0 or g.is_reloading:
            return
        g.ammo -= 1
        px, py = settings.PLAYER_POS
        base = math.atan2(target[1] - py, target[0] - px)
        mx = px + math.cos(base) * settings.MUZZLE_OFFSET
        my = py + math.sin(base) * settings.MUZZLE_OFFSET
        for _ in range(settings.PELLETS_PER_SHOT):
            a = base + random.uniform(-settings.PELLET_SPREAD, settings.PELLET_SPREAD)
            speed = random.uniform(*settings.PELLET_SPEED)
            g.pellets.append(
                {"pos": [mx, my], "vel": [math.cos(a) * speed, math.sin(a) * speed],
                 "life": settings.PELLET_LIFE}
            )

    def reload(self):
        g = self.m.game
        if g.is_reloading or g.ammo >= settings.AMMO_MAX or g.money < settings.RELOAD_COST:
            return
        g.money -= settings.RELOAD_COST
        g.is_reloading = True
        g.reload_timer = settings.RELOAD_FRAMES
        self.add_popup(f"-${settings.RELOAD_COST}", settings.PLAYER_POS, settings.ALERT_COLOR)

    # --- helpers ----------------------------------------------------------
    def add_popup(self, text, pos, color):
        self.m.game.popups.append({"text": text, "pos": [pos[0], pos[1]], "color": color, "life": 45})

    def spawn_duck(self):
        kind = random.choice(list(settings.DUCK_TYPES))
        cfg = settings.DUCK_TYPES[kind]
        self.m.game.ducks.append(
            {
                "pos": [random.randint(*settings.SPAWN_X_RANGE), -40],
                "speed": random.uniform(*cfg["speed"]),
                "radius": cfg["radius"],
                "reward": cfg["reward"],
                "sprite": self.m.assets["duck_" + kind],
            }
        )

    # --- update -----------------------------------------------------------
    def update(self):
        g = self.m.game

        if g.is_reloading:
            g.reload_timer -= 1
            if g.reload_timer <= 0:
                g.ammo = settings.AMMO_MAX
                g.is_reloading = False

        g.spawn_timer += 1
        if g.spawn_timer >= settings.SPAWN_INTERVAL:
            g.spawn_timer = 0
            self.spawn_duck()

        for p in g.pellets[:]:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["life"] -= 1
            if p["life"] <= 0:
                g.pellets.remove(p)

        for duck in g.ducks[:]:
            duck["pos"][1] += duck["speed"]

            hit = None
            for p in g.pellets:
                if math.hypot(p["pos"][0] - duck["pos"][0], p["pos"][1] - duck["pos"][1]) < duck["radius"]:
                    hit = p
                    break
            if hit:
                g.pellets.remove(hit)
                g.ducks.remove(duck)
                g.money += duck["reward"]
                g.ducks_shot += 1
                self.add_popup(f"+${duck['reward']}", duck["pos"], settings.GOLD_COLOR)
            elif duck["pos"][1] > settings.HEIGHT + 40:
                g.ducks.remove(duck)
                g.money -= settings.ESCAPE_PENALTY
                self.add_popup(f"-${settings.ESCAPE_PENALTY}", (duck["pos"][0], settings.HEIGHT - 30), settings.ALERT_COLOR)

        for pop in g.popups[:]:
            pop["pos"][1] -= 0.8
            pop["life"] -= 1
            if pop["life"] <= 0:
                g.popups.remove(pop)

        if g.is_bankrupt:
            self.m.end_session()

    # --- draw -------------------------------------------------------------
    def draw(self, surface, crosshair=True):
        g = self.m.game
        assets = self.m.assets
        fonts = self.m.fonts

        if assets["bg"]:
            surface.blit(assets["bg"], (0, 0))
        else:
            surface.fill((40, 40, 40))

        for duck in g.ducks:
            pos = (int(duck["pos"][0]), int(duck["pos"][1]))
            if duck["sprite"]:
                surface.blit(duck["sprite"], duck["sprite"].get_rect(center=pos))
            else:
                pygame.draw.circle(surface, settings.GOLD_COLOR, pos, duck["radius"])

        for p in g.pellets:
            pygame.draw.circle(surface, settings.PELLET_COLOR, (int(p["pos"][0]), int(p["pos"][1])), 3)

        mouse = pygame.mouse.get_pos()
        if assets["player"]:
            px, py = settings.PLAYER_POS
            angle = math.degrees(math.atan2(-(mouse[1] - py), mouse[0] - px))
            rotated = pygame.transform.rotate(assets["player"], angle)
            surface.blit(rotated, rotated.get_rect(center=settings.PLAYER_POS))

        for pop in g.popups:
            draw_text(surface, fonts, pop["text"], 28, pop["color"],
                      (int(pop["pos"][0]), int(pop["pos"][1])), "center")

        self.draw_hud(surface)
        if crosshair:
            self.draw_crosshair(surface, mouse)

    def draw_hud(self, surface):
        g = self.m.game
        fonts = self.m.fonts
        draw_text(surface, fonts, f"${g.money}", 40, settings.GOLD_COLOR, (20, 16))

        if g.is_reloading:
            text, color = "RELOADING...", settings.ALERT_COLOR
        elif g.ammo == 0:
            text, color = f"OUT OF AMMO - press R (${settings.RELOAD_COST})", settings.ALERT_COLOR
        else:
            text, color = f"AMMO {g.ammo}/{settings.AMMO_MAX}", settings.TEXT_COLOR
        draw_text(surface, fonts, text, 26, color, (22, 58))
        draw_text(surface, fonts, "R: reload   ESC: menu", 20, settings.MUTED_COLOR,
                  (settings.WIDTH - 20, 16), "topright")

    def draw_crosshair(self, surface, pos):
        x, y = pos
        pygame.draw.circle(surface, settings.WHITE, pos, 10, 2)
        pygame.draw.line(surface, settings.WHITE, (x - 16, y), (x - 6, y), 2)
        pygame.draw.line(surface, settings.WHITE, (x + 6, y), (x + 16, y), 2)
        pygame.draw.line(surface, settings.WHITE, (x, y - 16), (x, y - 6), 2)
        pygame.draw.line(surface, settings.WHITE, (x, y + 6), (x, y + 16), 2)
