import math
import os
import random
import pygame

# --- INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duckshot - Riverbank Defense")
clock = pygame.time.Clock()

# --- COLORS ---
PELLET_COLOR = (255, 255, 200)
TEXT_COLOR = (255, 255, 255)
ALERT_COLOR = (255, 80, 80)
GOLD_COLOR = (255, 215, 0)


# --- ASSET PROCESSING ---
def load_and_prep_assets():
    assets = {"bg": None, "player": None, "duck_mallard": None, "duck_yellow": None}

    # 1. Load Background Image
    bg_path = os.path.join("assets", "river_bg_2.jpg")
    if os.path.exists(bg_path):
        raw_bg = pygame.image.load(bg_path).convert()
        assets["bg"] = pygame.transform.scale(raw_bg, (WIDTH, HEIGHT))

    # 2. Load Player Sprite
    player_path = os.path.join("assets", "player.png")
    if os.path.exists(player_path):
        raw_player = pygame.image.load(player_path).convert_alpha()
        assets["player"] = pygame.transform.scale(raw_player, (64, 64))

    # 3. Process & Chroma-Key Duck Sheet
    duck_path = os.path.join("assets", "duckling_sheet.png")
    if os.path.exists(duck_path):
        sheet = pygame.image.load(duck_path).convert()

        # Dynamic Chroma Keying (reads gray background color from top-left pixel)
        bg_key_color = sheet.get_at((0, 0))
        sheet.set_colorkey(bg_key_color)

        sw, sh = sheet.get_size()
        half_h = sh // 2

        # Crop Top Duck (Mallard)
        mallard_crop = sheet.subsurface(pygame.Rect(0, 0, sw, half_h))
        assets["duck_mallard"] = pygame.transform.scale(mallard_crop, (42, 54))

        # Crop Bottom Duck (Yellow Swarmer)
        yellow_crop = sheet.subsurface(pygame.Rect(0, half_h, sw, half_h))
        assets["duck_yellow"] = pygame.transform.scale(yellow_crop, (36, 48))

    return assets


ASSETS = load_and_prep_assets()

# --- GAME ECONOMY & STATE ---
player_pos = [670, 480]  # Stationed on the right bank dirt track
money = 100
RELOAD_COST = 10
ammo_max = 6
ammo = ammo_max
is_reloading = False
reload_timer = 0
game_over = False

ducks = []
pellets = []
spawn_timer = 0
SPAWN_INTERVAL = 65


def spawn_duck():
    # River bounds (X coordinates 230 to 570)
    x_pos = random.randint(230, 570)
    duck_type = random.choice(["mallard", "yellow"])

    if duck_type == "mallard":
        speed = random.uniform(2.0, 3.2)
        reward = 15
        radius = 20
        sprite = ASSETS["duck_mallard"]
    else:
        speed = random.uniform(3.8, 5.2)
        reward = 25
        radius = 16
        sprite = ASSETS["duck_yellow"]

    ducks.append(
        {
            "pos": [x_pos, -40],
            "speed": speed,
            "radius": radius,
            "reward": reward,
            "type": duck_type,
            "sprite": sprite,
        }
    )


def fire_shotgun(target_pos):
    global ammo
    if ammo <= 0 or is_reloading or game_over:
        return

    ammo -= 1
    dx = target_pos[0] - player_pos[0]
    dy = target_pos[1] - player_pos[1]
    base_angle = math.atan2(dy, dx)

    for _ in range(7):
        spread = base_angle + random.uniform(-0.16, 0.16)
        speed = random.uniform(16, 22)
        vel = [math.cos(spread) * speed, math.sin(spread) * speed]
        pellets.append({"pos": list(player_pos), "vel": vel, "life": 32})


font = pygame.font.SysFont("Consolas", 22, bold=True)
running = True

while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    # --- INPUT PROCESSING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            fire_shotgun(mouse_pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not is_reloading and not game_over:
                if ammo < ammo_max and money >= RELOAD_COST:
                    money -= RELOAD_COST
                    is_reloading = True
                    reload_timer = 35

    if not game_over:
        # Reloading Logic
        if is_reloading:
            reload_timer -= 1
            if reload_timer <= 0:
                ammo = ammo_max
                is_reloading = False

        # Duck Spawning
        spawn_timer += 1
        if spawn_timer >= SPAWN_INTERVAL:
            spawn_duck()
            spawn_timer = 0

        # Pellet Movement
        for p in pellets[:]:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["life"] -= 1
            if p["life"] <= 0:
                pellets.remove(p)

        # Duck Movement & Collision
        for duck in ducks[:]:
            duck["pos"][1] += duck["speed"]

            for p in pellets[:]:
                dist = math.hypot(
                    p["pos"][0] - duck["pos"][0], p["pos"][1] - duck["pos"][1]
                )
                if dist < duck["radius"]:
                    money += duck["reward"]
                    if p in pellets:
                        pellets.remove(p)
                    if duck in ducks:
                        ducks.remove(duck)
                    break

            # Escape penalty
            if duck["pos"][1] > HEIGHT + 40:
                money -= 20
                ducks.remove(duck)
                if money < 0:
                    game_over = True

    # --- RENDERING ---
    # Draw River Background Image
    if ASSETS["bg"]:
        screen.blit(ASSETS["bg"], (0, 0))
    else:
        screen.fill((40, 40, 40))

    # Draw Ducks
    for duck in ducks:
        if duck["sprite"]:
            rect = duck["sprite"].get_rect(
                center=(int(duck["pos"][0]), int(duck["pos"][1]))
            )
            screen.blit(duck["sprite"], rect)
        else:
            pygame.draw.circle(
                screen,
                GOLD_COLOR,
                (int(duck["pos"][0]), int(duck["pos"][1])),
                duck["radius"],
            )

    # Draw Shotgun Pellets
    for p in pellets:
        pygame.draw.circle(
            screen, PELLET_COLOR, (int(p["pos"][0]), int(p["pos"][1])), 3
        )

    # Draw Player Sprite
    if ASSETS["player"]:
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        rotated_player = pygame.transform.rotate(ASSETS["player"], angle)
        rect = rotated_player.get_rect(center=player_pos)
        screen.blit(rotated_player, rect)

    # --- HUD OVERLAY ---
    money_surface = font.render(f"MONEY: ${money}", True, GOLD_COLOR)
    screen.blit(money_surface, (20, 20))

    if is_reloading:
        ammo_txt = "RELOADING..."
        ammo_color = ALERT_COLOR
    elif ammo == 0:
        ammo_txt = "OUT OF AMMO! Press [R] ($10)"
        ammo_color = ALERT_COLOR
    else:
        ammo_txt = f"AMMO: {ammo}/{ammo_max} (Press [R] to Reload - ${RELOAD_COST})"
        ammo_color = TEXT_COLOR

    ammo_surface = font.render(ammo_txt, True, ammo_color)
    screen.blit(ammo_surface, (20, 50))

    if game_over:
        go_surface = font.render("BANKRUPT! GAME OVER", True, ALERT_COLOR)
        screen.blit(go_surface, (WIDTH // 2 - 120, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()