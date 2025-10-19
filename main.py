import pygame
import random
import math
import os

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


# Initialize Pygame
pygame.init()
pygame.mixer.init() # Initialize the mixer

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Star Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 128)   # A brighter, more minty green
YELLOW = (255, 255, 0)
RED = (255, 50, 50)     # A slightly softer red
BLUE = (100, 100, 255)  # A lighter blue
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Sounds - ADD YOUR SOUND FILES HERE
# Make sure you have .wav or .ogg files with these names in the assets/sounds directory
sound_dir = os.path.join(os.path.dirname(__file__), "assets", "sounds")
try:
    laser_sound = pygame.mixer.Sound(os.path.join(sound_dir, "laser.wav"))
    missile_sound = pygame.mixer.Sound(os.path.join(sound_dir, "missile.wav"))
    explosion_sound = pygame.mixer.Sound(os.path.join(sound_dir, "explosion.wav"))
    warp_sound = pygame.mixer.Sound(os.path.join(sound_dir, "warp.wav"))
    game_over_sound = pygame.mixer.Sound(os.path.join(sound_dir, "game_over.wav"))
    win_sound = pygame.mixer.Sound(os.path.join(sound_dir, "win.wav"))
    shield_hit_sound = pygame.mixer.Sound(os.path.join(sound_dir, "shield_hit.wav"))
except FileNotFoundError:
    print("Warning: Sound files not found. Continuing without sound.")
    laser_sound = None
    missile_sound = None
    explosion_sound = None
    warp_sound = None
    game_over_sound = None
    win_sound = None
    shield_hit_sound = None


# Player
player_angle = 0
player_rotation_speed = 0
player_speed = 0
player_grid_x = 4
player_grid_y = 4
player_energy = 1000
MAX_ENERGY = 1000
player_missiles = 5
ship_systems = {'radar': 100, 'computer': 100, 'engine': 100}
score = 0
high_score = load_high_score()

# Planets
planets = []
keys_collected_count = 0
boss = None

# Game State
game_state = 'menu' # playing, won, lost, map, menu
warp_targeting = False
target_grid_x = player_grid_x
target_grid_y = player_grid_y
date = 0
MAX_DATE = 1000
asteroid_fields = []
asteroids = []
shield_hit_particles = []
target_cursor_x = 0
target_cursor_y = 0

# Grid
GRID_SIZE = 8

# Starfield
stars = []
for _ in range(200):
    x = random.randint(-SCREEN_WIDTH, SCREEN_WIDTH)
    y = random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
    z = random.randint(1, SCREEN_WIDTH)
    color = random.choice([WHITE, YELLOW, (200, 200, 255)])
    brightness = random.uniform(0.5, 1.0)
    stars.append([x, y, z, color, brightness])

# Warp effect
warp_effect = 0
damage_effect = 0

# Bullets
bullets = []
missiles = []

# Explosions
explosions = []

# Enemy Bullets
enemy_bullets = []

# Enemies
enemies = []
enemy_type = random.choice(['fighter', 'bomber', 'cruiser'])
health = {'fighter': 10, 'bomber': 20, 'cruiser': 50}[enemy_type]
enemies.append({'x': 0, 'y': 0, 'z': 200, 'type': enemy_type, 'grid_x': player_grid_x, 'grid_y': player_grid_y, 'health': health}) # Add one enemy

# Bases
bases = []
bases.append({'x': 1, 'y': 1, 'health': 100})



def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def reset_game(mode='adventure'):
    global player_angle, player_rotation_speed, player_speed, player_grid_x, player_grid_y, player_energy, player_missiles, game_state, warp_targeting, target_grid_x, target_grid_y, stars, bullets, missiles, explosions, enemy_bullets, enemies, bases, score, planets, keys_collected_count, boss, date, target_cursor_x, target_cursor_y, asteroid_fields, asteroids, shield_hit_particles, ship_systems
    player_angle = 0
    player_rotation_speed = 0
    player_speed = 0
    player_grid_x = 4
    player_grid_y = 4
    player_energy = 1000
    player_missiles = 5
    ship_systems = {'radar': 100, 'computer': 100, 'engine': 100}
    score = 0
    game_state = 'playing' # Always start in playing state after menu selection
    warp_targeting = False
    target_grid_x = player_grid_x
    target_grid_y = player_grid_y
    target_cursor_x = player_grid_x
    target_cursor_y = player_grid_y
    stars = []
    for _ in range(200):
        x = random.randint(-SCREEN_WIDTH, SCREEN_WIDTH)
        y = random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
        z = random.randint(1, SCREEN_WIDTH)
        color = random.choice([WHITE, YELLOW, (200, 200, 255)])
        brightness = random.uniform(0.5, 1.0)
        stars.append([x, y, z, color, brightness])
    bullets = []
    missiles = []
    explosions = []
    enemy_bullets = []
    enemies = []
    bases = []
    bases.append({'x': 1, 'y': 1, 'health': 100})
    bases.append({'x': 6, 'y': 6, 'health': 100})
    planets = []
    keys_collected_count = 0
    boss = None
    date = 0
    asteroid_fields = []
    shield_hit_particles = []

    if mode == 'adventure':
        # Create 7 planets with keys
        while len(planets) < 7:
            planet_x = random.randint(0, GRID_SIZE - 1)
            planet_y = random.randint(0, GRID_SIZE - 1)
            is_on_base = any(base['x'] == planet_x and base['y'] == planet_y for base in bases)
            is_on_player_start = (planet_x == 4 and planet_y == 4)
            is_duplicate = any(p['x'] == planet_x and p['y'] == planet_y for p in planets)
            if not is_on_base and not is_on_player_start and not is_duplicate:
                planets.append({'x': planet_x, 'y': planet_y, 'has_key': True})

        # Create some more planets without keys
        while len(planets) < 15:
            planet_x = random.randint(0, GRID_SIZE - 1)
            planet_y = random.randint(0, GRID_SIZE - 1)
            is_on_base = any(base['x'] == planet_x and base['y'] == planet_y for base in bases)
            is_on_player_start = (planet_x == 4 and planet_y == 4)
            is_duplicate = any(p['x'] == planet_x and p['y'] == planet_y for p in planets)
            if not is_on_base and not is_on_player_start and not is_duplicate:
                planets.append({'x': planet_x, 'y': planet_y, 'has_key': False})
        
        # Initial enemy for adventure mode
        enemy_type = random.choice(['fighter', 'bomber', 'cruiser'])
        health = {'fighter': 10, 'bomber': 20, 'cruiser': 50}[enemy_type]
        enemies.append({'x': 0, 'y': 0, 'z': 200, 'type': enemy_type, 'grid_x': player_grid_x, 'grid_y': player_grid_y, 'health': health})

        # Asteroid fields for adventure mode
        while len(asteroid_fields) < 3:
            ax = random.randint(0, GRID_SIZE - 1)
            ay = random.randint(0, GRID_SIZE - 1)
            is_on_base = any(base['x'] == ax and base['y'] == ay for base in bases)
            is_on_planet = any(p['x'] == ax and p['y'] == ay for p in planets)
            is_on_player_start = (ax == 4 and ay == 4)
            is_duplicate = any(af['x'] == ax and af['y'] == ay for af in asteroid_fields)
            if not is_on_base and not is_on_planet and not is_on_player_start and not is_duplicate:
                asteroid_fields.append({'x': ax, 'y': ay})

    elif mode == 'command':
        # Command mode specific initialization
        # More enemies, focus on defending bases
        for _ in range(5): # 5 initial enemies
            enemy_type = random.choice(['fighter', 'bomber', 'cruiser'])
            health = {'fighter': 10, 'bomber': 20, 'cruiser': 50}[enemy_type]
            enemies.append({'x': random.randint(-100, 100), 'y': random.randint(-100, 100), 'z': random.randint(200, 500), 'type': enemy_type, 'grid_x': random.randint(0, GRID_SIZE - 1), 'grid_y': random.randint(0, GRID_SIZE - 1), 'health': health})
        # No keys, no boss in command mode
        planets = []
        keys_collected_count = 0
        boss = None
        # No asteroid fields in command mode for simplicity
        asteroid_fields = []

    elif mode == 'training':
        # Training mode specific initialization
        # Few enemies, no objectives
        for _ in range(2): # 2 initial enemies
            enemy_type = random.choice(['fighter', 'cruiser']) # No bombers in training
            health = {'fighter': 10, 'bomber': 20, 'cruiser': 50}[enemy_type]
            enemies.append({'x': random.randint(-100, 100), 'y': random.randint(-100, 100), 'z': random.randint(200, 500), 'type': enemy_type, 'grid_x': random.randint(0, GRID_SIZE - 1), 'grid_y': random.randint(0, GRID_SIZE - 1), 'health': health})
        # No keys, no boss, no bases, no asteroid fields in training mode
        planets = []
        keys_collected_count = 0
        boss = None
        bases = []
        asteroid_fields = []

def draw_star_map():
    screen.fill(BLACK)
    
    # Draw grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pygame.draw.rect(screen, GREEN, (x * 100, y * 75, 100, 75), 1)

    # Draw bases
    for base in bases:
        base_map_x = base['x'] * 100 + 50
        base_map_y = base['y'] * 75 + 37
        health_ratio = base['health'] / 100.0
        if health_ratio > 0.5:
            color = BLUE
        elif health_ratio > 0.2:
            color = YELLOW
        else:
            color = RED
        pygame.draw.circle(screen, color, (base_map_x, base_map_y), 10)

    # Draw planets
    for p in planets:
        planet_map_x = p['x'] * 100 + 50
        planet_map_y = p['y'] * 75 + 37
        if p['has_key']:
            pygame.draw.rect(screen, YELLOW, (planet_map_x - 5, planet_map_y - 5, 10, 10))
        elif p.get('is_final'):
            pygame.draw.circle(screen, MAGENTA, (planet_map_x, planet_map_y), 12)

    # Draw asteroid fields
    for af in asteroid_fields:
        af_map_x = af['x'] * 100 + 50
        af_map_y = af['y'] * 75 + 37
        pygame.draw.circle(screen, (128, 128, 128), (af_map_x, af_map_y), 10)

    # Draw player
    player_map_x = player_grid_x * 100 + 50
    player_map_y = player_grid_y * 75 + 37
    pygame.draw.circle(screen, YELLOW, (player_map_x, player_map_y), 5)
    heading_x = player_map_x + 20 * math.sin(math.radians(player_angle))
    heading_y = player_map_y - 20 * math.cos(math.radians(player_angle))
    pygame.draw.line(screen, YELLOW, (player_map_x, player_map_y), (heading_x, heading_y), 2)

    # Draw enemies
    for enemy in enemies:
        enemy_map_x = enemy['grid_x'] * 100 + 50
        enemy_map_y = enemy['grid_y'] * 75 + 37
        if enemy['type'] == 'fighter':
            pygame.draw.circle(screen, RED, (enemy_map_x, enemy_map_y), 3)
        elif enemy['type'] == 'bomber':
            pygame.draw.rect(screen, ORANGE, (enemy_map_x - 3, enemy_map_y - 3, 6, 6))
        elif enemy['type'] == 'boss':
            pygame.draw.circle(screen, MAGENTA, (enemy_map_x, enemy_map_y), 8)

    # Draw cursor
    pygame.draw.rect(screen, WHITE, (target_cursor_x * 100, target_cursor_y * 75, 100, 75), 2)



def draw_cockpit_frame():
    # A more detailed, Star Luster-style cockpit
    cockpit_color = (0, 100, 0) # Dark green
    # Top and bottom bars
    pygame.draw.rect(screen, cockpit_color, (0, 0, SCREEN_WIDTH, 100))
    pygame.draw.rect(screen, cockpit_color, (0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150))
    # Side bars
    pygame.draw.rect(screen, cockpit_color, (0, 100, 100, SCREEN_HEIGHT - 250))
    pygame.draw.rect(screen, cockpit_color, (SCREEN_WIDTH - 100, 100, 100, SCREEN_HEIGHT - 250))
    # Window outline
    pygame.draw.rect(screen, GREEN, (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 250), 5)

def draw_hud():
    font = pygame.font.Font(None, 30)
    
    # --- Left Side ---
    # Energy Gauge (as an arc)
    energy_angle = (player_energy / MAX_ENERGY) * 180
    pygame.draw.arc(screen, GREEN, (10, SCREEN_HEIGHT - 140, 80, 80), math.radians(180), math.radians(180 + energy_angle), 5)
    energy_text = font.render("ENERGY", True, WHITE)
    screen.blit(energy_text, (20, SCREEN_HEIGHT - 130))

    # System Status
    system_font = pygame.font.Font(None, 24)
    for i, (system, health) in enumerate(ship_systems.items()):
        color = GREEN if health > 50 else (YELLOW if health > 20 else RED)
        text = system_font.render(f"{system.upper()}: {health}%", True, color)
        screen.blit(text, (10, 110 + i * 25))

    # --- Right Side ---
    # Missile Count (as vertical bars)
    missile_text = font.render("MISSILES", True, WHITE)
    screen.blit(missile_text, (SCREEN_WIDTH - 95, SCREEN_HEIGHT - 130))
    for i in range(player_missiles):
        pygame.draw.rect(screen, CYAN, (SCREEN_WIDTH - 80 + (i * 10), SCREEN_HEIGHT - 100, 5, 20))

    # --- Top Center ---
    # Score
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, 30))
    screen.blit(score_text, score_rect)
    # High Score
    high_score_text = font.render(f"HIGH: {high_score}", True, YELLOW)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH/2, 60))
    screen.blit(high_score_text, high_score_rect)

    # --- Bottom Center ---
    # Date
    date_text = font.render(f"DATE: {date}", True, WHITE)
    date_rect = date_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 20))
    screen.blit(date_text, date_rect)
    # Keys
    key_text = font.render(f"KEYS: {keys_collected_count}/7", True, YELLOW)
    key_rect = key_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50))
    screen.blit(key_text, key_rect)

def draw_radar():
    radar_x = SCREEN_WIDTH / 2
    radar_y = SCREEN_HEIGHT - 75
    radar_radius = 70
    
    # Radar dish
    pygame.draw.circle(screen, (0, 50, 0), (radar_x, radar_y), radar_radius)
    
    if ship_systems['radar'] == 0:
        # Radar is out
        font = pygame.font.Font(None, 24)
        text = font.render("RADAR OUT", True, RED)
        text_rect = text.get_rect(center=(radar_x, radar_y))
        screen.blit(text, text_rect)
        return

    # Radar sweep
    sweep_angle = (pygame.time.get_ticks() % 3000) / 3000 * 360
    sweep_end_x = radar_x + radar_radius * math.cos(math.radians(sweep_angle - 90))
    sweep_end_y = radar_y + radar_radius * math.sin(math.radians(sweep_angle - 90))
    pygame.draw.line(screen, GREEN, (radar_x, radar_y), (sweep_end_x, sweep_end_y), 2)

    # Radar grid
    pygame.draw.circle(screen, GREEN, (radar_x, radar_y), radar_radius, 1)
    pygame.draw.circle(screen, GREEN, (radar_x, radar_y), radar_radius / 2, 1)
    pygame.draw.line(screen, GREEN, (radar_x - radar_radius, radar_y), (radar_x + radar_radius, radar_y), 1)
    pygame.draw.line(screen, GREEN, (radar_x, radar_y - radar_radius), (radar_x, radar_y + radar_radius), 1)

    # Player in center
    pygame.draw.circle(screen, YELLOW, (radar_x, radar_y), 3)

    # Draw objects on radar
    if ship_systems['radar'] < 20:
        # Only player is visible
        return

    if ship_systems['radar'] < 50 and random.random() < 0.5:
        # Flickering effect
        return

    # Enemies
    for enemy in enemies:
        if enemy['grid_x'] == player_grid_x and enemy['grid_y'] == player_grid_y:
            # Calculate relative position
            rel_x = enemy['x']
            rel_z = enemy['z']
            
            # Rotate with player's view
            rotated_x = rel_x * math.cos(math.radians(player_angle)) - rel_z * math.sin(math.radians(player_angle))
            rotated_z = rel_x * math.sin(math.radians(player_angle)) + rel_z * math.cos(math.radians(player_angle))

            # Scale to radar
            radar_dist = math.sqrt(rotated_x**2 + rotated_z**2)
            if radar_dist < 500: # Only show enemies within a certain range
                angle = math.atan2(rotated_x, -rotated_z)
                display_dist = (radar_dist / 500) * radar_radius
                
                blip_x = radar_x + display_dist * math.sin(angle)
                blip_y = radar_y + display_dist * math.cos(angle)
                
                if enemy['type'] == 'boss':
                    color = MAGENTA
                else:
                    color = RED
                pygame.draw.circle(screen, color, (blip_x, blip_y), 3)



def draw_warp_effect():
    screen.fill(BLACK)
    for star in stars:
        # Move stars from center to edge
        star[2] -= warp_effect * 2
        if star[2] < 1:
            star[0] = random.randint(-SCREEN_WIDTH, SCREEN_WIDTH)
            star[1] = random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
            star[2] = SCREEN_WIDTH

        k = 128.0 / star[2] if star[2] != 0 else 128.0
        x = int(star[0] * k + SCREEN_WIDTH / 2)
        y = int(star[1] * k + SCREEN_HEIGHT / 2)

        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            size = (1 - star[2] / SCREEN_WIDTH) * 5
            pygame.draw.circle(screen, WHITE, (x, y), size)



# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == 'playing':
            if event.type == pygame.KEYDOWN:
                if warp_targeting:
                    if event.key == pygame.K_LEFT:
                        target_grid_x = max(0, target_grid_x - 1)
                    if event.key == pygame.K_RIGHT:
                        target_grid_x = min(GRID_SIZE - 1, target_grid_x + 1)
                    if event.key == pygame.K_UP:
                        target_grid_y = max(0, target_grid_y - 1)
                    if event.key == pygame.K_DOWN:
                        target_grid_y = min(GRID_SIZE - 1, target_grid_y + 1)
                else:
                    if event.key == pygame.K_LEFT:
                        player_rotation_speed = 6
                    if event.key == pygame.K_RIGHT:
                        player_rotation_speed = -6
                    if event.key == pygame.K_UP:
                        player_speed = 10
                    if event.key == pygame.K_DOWN:
                        player_speed = -10
                if event.key == pygame.K_w:
                    if ship_systems['computer'] >= 50:
                        warp_targeting = not warp_targeting
                        if not warp_targeting: # if we are turning warp off
                            dist = math.sqrt((target_grid_x - player_grid_x)**2 + (target_grid_y - player_grid_y)**2)
                            energy_cost = int(dist * 10)
                            if player_energy >= energy_cost:
                                if warp_sound: warp_sound.play()
                                player_energy -= energy_cost
                                date += int(dist)
                                warp_effect = 10 # Start warp effect
                                player_grid_x = target_grid_x
                                player_grid_y = target_grid_y
                                asteroids = []
                        else: # if we are turning warp on
                            target_grid_x = player_grid_x
                            target_grid_y = player_grid_y
                            for af in asteroid_fields:
                                if af['x'] == player_grid_x and af['y'] == player_grid_y:
                                    for _ in range(20):
                                        asteroids.append({
                                            'x': random.randint(-500, 500),
                                            'y': random.randint(-300, 300),
                                            'z': random.randint(100, 1000),
                                            'size': random.randint(10, 40)
                                        })
                                    break
                            # Add a new enemy when warping to a new sector
                            if not any(base['x'] == player_grid_x and base['y'] == player_grid_y for base in bases):
                                enemy_type = random.choice(['fighter', 'bomber', 'cruiser'])
                                health = {'fighter': 10, 'bomber': 20, 'cruiser': 50}[enemy_type]
                                enemies.append({'x': random.randint(-100, 100), 'y': random.randint(-100, 100), 'z': 500, 'type': enemy_type, 'grid_x': target_grid_x, 'grid_y': target_grid_y, 'health': health})
                if event.key == pygame.K_SPACE:
                    if player_energy >= 10:
                        if laser_sound: laser_sound.play()
                        player_energy -= 10
                        bullets.append({'x': 0, 'y': 0, 'z': 0, 'vx': 0, 'vy': 0, 'vz': 40})
                if event.key == pygame.K_n:
                    if player_missiles > 0:
                        if missile_sound: missile_sound.play()
                        player_missiles -= 1
                        missiles.append({'x': 0, 'y': 0, 'z': 0, 'vx': 0, 'vy': 0, 'vz': 10})
                if event.key == pygame.K_m:
                    game_state = 'map'
                if event.key == pygame.K_h:
                    if ship_systems['computer'] > 0 and player_energy >= 50:
                        if warp_sound: warp_sound.play()
                        player_energy -= 50
                        date += 5
                        warp_effect = 10 # Start warp effect
                        player_grid_x = random.randint(0, GRID_SIZE - 1)
                        player_grid_y = random.randint(0, GRID_SIZE - 1)
                        asteroids = []
                        for af in asteroid_fields:
                            if af['x'] == player_grid_x and af['y'] == player_grid_y:
                                for _ in range(20):
                                    asteroids.append({
                                        'x': random.randint(-500, 500),
                                        'y': random.randint(-300, 300),
                                        'z': random.randint(100, 1000),
                                        'size': random.randint(10, 40)
                                    })
                                break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_rotation_speed = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_speed = 0
        elif game_state == 'map':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    game_state = 'playing'
                if event.key == pygame.K_LEFT:
                    target_cursor_x = max(0, target_cursor_x - 1)
                if event.key == pygame.K_RIGHT:
                    target_cursor_x = min(GRID_SIZE - 1, target_cursor_x + 1)
                if event.key == pygame.K_UP:
                    target_cursor_y = max(0, target_cursor_y - 1)
                if event.key == pygame.K_DOWN:
                    target_cursor_y = min(GRID_SIZE - 1, target_cursor_y + 1)
                if event.key == pygame.K_SPACE:
                    if player_missiles > 0:
                        player_missiles -= 1
                        # Find an enemy in the target sector and destroy it
                        for enemy in enemies:
                            if enemy['grid_x'] == target_cursor_x and enemy['grid_y'] == target_cursor_y:
                                enemies.remove(enemy)
                                score += 10 # Or some other score
                                if explosion_sound: explosion_sound.play()
                                break # Destroy one enemy per missile
        elif game_state == 'lost':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = 'menu' # Go back to menu after game over

    if game_state == 'playing':
        # Update player rotation and position
        player_angle += player_rotation_speed
        
        if ship_systems['engine'] == 0:
            engine_efficiency = 0
        elif ship_systems['engine'] < 50:
            engine_efficiency = (ship_systems['engine'] / 100.0) * 0.5 # Max 25% efficiency
        else:
            engine_efficiency = ship_systems['engine'] / 100.0

        dx = -player_speed * math.sin(math.radians(player_angle)) * engine_efficiency
        dz = -player_speed * math.cos(math.radians(player_angle)) * engine_efficiency

        for star in stars:
            star[0] -= dx
            star[2] -= dz
        for enemy in enemies:
            enemy['x'] -= dx
            enemy['z'] -= dz
        for asteroid in asteroids:
            asteroid['x'] -= dx
            asteroid['z'] -= dz



        # Update bullets and missiles
        for projectile in bullets + missiles:
            projectile['z'] += projectile['vz']
            if projectile['z'] > 1000:
                if projectile in bullets:
                    bullets.remove(projectile)
                else:
                    missiles.remove(projectile)

        # Update enemy bullets
        for bullet in enemy_bullets:
            bullet['z'] += bullet['vz']
            if bullet['z'] < -100:
                enemy_bullets.remove(bullet)

        # Update explosions
        for explosion in explosions:
            explosion['radius'] += 1
            explosion['alpha'] -= 10
            if explosion['alpha'] <= 0:
                explosions.remove(explosion)
                continue # Skip drawing if explosion is gone

            # Update particles
            for particle in explosion['particles']:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['z'] += particle['vz']
                particle['alpha'] -= 15 # Particles fade faster


        # Update enemies
        for enemy in enemies:
            if enemy['type'] == 'boss':
                # Move towards player on the grid
                if enemy['grid_x'] < player_grid_x:
                    enemy['grid_x'] += 1
                elif enemy['grid_x'] > player_grid_x:
                    enemy['grid_x'] -= 1
                if enemy['grid_y'] < player_grid_y:
                    enemy['grid_y'] += 1
                elif enemy['grid_y'] > player_grid_y:
                    enemy['grid_y'] -= 1
                
                # If boss reaches player's grid, game over
                if enemy['grid_x'] == player_grid_x and enemy['grid_y'] == player_grid_y:
                    if game_over_sound: game_over_sound.play()
                    game_state = 'lost'
            elif enemy['type'] == 'fighter':
                enemy['z'] -= 0.5 # Fighters are faster
                # Fighters shoot at the player
                if random.random() < 0.01:
                    enemy_bullets.append({'x': enemy['x'], 'y': enemy['y'], 'z': enemy['z'], 'vx': 0, 'vy': 0, 'vz': -10})
            elif enemy['type'] == 'bomber':
                base_in_sector = None
                for base in bases:
                    if player_grid_x == base['x'] and player_grid_y == base['y']:
                        base_in_sector = base
                        break
                if base_in_sector:
                    # Fly towards base
                    enemy['z'] -= 0.25
                    if enemy['z'] < 0:
                        base_in_sector['health'] -= 10
                        if enemy in enemies: enemies.remove(enemy)
                        if base_in_sector['health'] <= 0:
                            if game_over_sound: game_over_sound.play()
                            game_state = 'lost'
                else:
                    enemy['z'] -= 0.25
            elif enemy['type'] == 'cruiser':
                enemy['z'] -= 0.1 # Cruisers are slow
                # Cruisers shoot powerful shots less frequently
                if random.random() < 0.005:
                    enemy_bullets.append({'x': enemy['x'], 'y': enemy['y'], 'z': enemy['z'], 'vx': 0, 'vy': 0, 'vz': -5, 'power': 20}) # More power

            if enemy['z'] < 0:
                if enemy in enemies: 
                    if shield_hit_sound: shield_hit_sound.play()
                    enemies.remove(enemy)
                    player_energy -= 10
                    damage_effect = 10



        # Collision detection
        for projectile in bullets + missiles:
            for enemy in enemies:
                dist = math.sqrt((projectile['x'] - enemy['x'])**2 + (projectile['y'] - enemy['y'])**2 + (projectile['z'] - enemy['z'])**2)
                if dist < 40:
                    if explosion_sound: explosion_sound.play()
                    explosions.append({
                        'x': enemy['x'], 
                        'y': enemy['y'], 
                        'z': enemy['z'], 
                        'radius': 10, 
                        'alpha': 255,
                        'particles': []
                    })
                    # Generate particles
                    for _ in range(20):
                        explosions[-1]['particles'].append({
                            'x': 0, 'y': 0, 'z': 0,
                            'vx': random.uniform(-10, 10),
                            'vy': random.uniform(-10, 10),
                            'vz': random.uniform(-10, 10),
                            'color': random.choice([RED, ORANGE, YELLOW, WHITE]),
                            'size': random.randint(2, 5),
                            'alpha': 255
                        })
                    
                    if projectile in bullets:
                        damage = 10
                    else: # missile
                        damage = 50
                    
                    enemy['health'] -= damage

                    if enemy['health'] <= 0:
                        if enemy['type'] == 'boss':
                            if win_sound: win_sound.play()
                            game_state = 'won'
                            score += 1000
                        elif enemy['type'] == 'fighter':
                            score += 10
                        elif enemy['type'] == 'bomber':
                            score += 20
                        elif enemy['type'] == 'cruiser':
                            score += 50
                        enemies.remove(enemy)

                    if projectile in bullets:
                        bullets.remove(projectile)
                    else:
                        missiles.remove(projectile)
                    
                    break

        # Collision detection for enemy bullets
        for bullet in enemy_bullets:
            dist = math.sqrt(bullet['x']**2 + bullet['y']**2 + bullet['z']**2)
            if dist < 20:
                if shield_hit_sound: shield_hit_sound.play()
                enemy_bullets.remove(bullet)
                if random.random() < 0.3: # 30% chance to damage a system
                    system_to_damage = random.choice(list(ship_systems.keys()))
                    ship_systems[system_to_damage] -= 10
                    if ship_systems[system_to_damage] < 0:
                        ship_systems[system_to_damage] = 0
                else:
                    player_energy -= bullet.get('power', 5)
                damage_effect = 10 # Red overlay

        # Asteroid Collision
        for asteroid in asteroids:
            dist = math.sqrt(asteroid['x']**2 + asteroid['y']**2 + asteroid['z']**2)
            if dist < asteroid['size']:
                if shield_hit_sound: shield_hit_sound.play()
                if random.random() < 0.3: # 30% chance to damage a system
                    system_to_damage = random.choice(list(ship_systems.keys()))
                    ship_systems[system_to_damage] -= 20 # Asteroids do more damage
                    if ship_systems[system_to_damage] < 0:
                        ship_systems[system_to_damage] = 0
                else:
                    player_energy -= 10
                damage_effect = 10 # Red overlay
                asteroids.remove(asteroid)

        
        # Docking and refueling
        for base in bases:
            if player_grid_x == base['x'] and player_grid_y == base['y']:
                player_energy += 5
                if player_energy > MAX_ENERGY:
                    player_energy = MAX_ENERGY
                player_missiles = 5 # Refill missiles at base
                # Repair systems
                for system in ship_systems:
                    if ship_systems[system] < 100:
                        ship_systems[system] += 0.5
                        if ship_systems[system] > 100:
                            ship_systems[system] = 100



        # Check for game over
        if player_energy <= 0 or date >= MAX_DATE:
            if game_over_sound: game_over_sound.play()
            game_state = 'lost'

        # Key Collection from planets
        for p in planets:
            if player_grid_x == p['x'] and player_grid_y == p['y'] and p['has_key']:
                p['has_key'] = False
                keys_collected_count += 1
                # Spawn boss if all keys are collected
                if keys_collected_count == 7:
                    final_planet_x = random.randint(0, GRID_SIZE - 1)
                    final_planet_y = random.randint(0, GRID_SIZE - 1)
                    planets.append({'x': final_planet_x, 'y': final_planet_y, 'has_key': False, 'is_final': True})
                    boss = {'x': random.randint(-100, 100), 'y': random.randint(-100, 100), 'z': 1000, 'type': 'boss', 'grid_x': final_planet_x, 'grid_y': final_planet_y, 'health': 100}
                    enemies.append(boss)


    # Drawing
    if warp_effect > 0:
        draw_warp_effect()
        warp_effect -= 1
    else:
        screen.fill(BLACK)

    if game_state == 'playing':
        # Draw Starfield
        for star in stars:
            star[0] -= player_rotation_speed * 0.1
            
            k = 128.0 / star[2] if star[2] != 0 else 128.0
            x = int(star[0] * k + SCREEN_WIDTH / 2)
            y = int(star[1] * k + SCREEN_HEIGHT / 2)

            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                # Twinkling effect
                twinkle = random.uniform(0.5, 1.0)
                final_brightness = star[4] * twinkle
                final_color = (int(star[3][0] * final_brightness), int(star[3][1] * final_brightness), int(star[3][2] * final_brightness))
                
                size = (1 - star[2] / SCREEN_WIDTH) * 3
                pygame.draw.circle(screen, final_color, (x, y), size)

            if star[0] < -SCREEN_WIDTH:
                star[0] = SCREEN_WIDTH
            if star[0] > SCREEN_WIDTH:
                star[0] = -SCREEN_WIDTH

        # Draw Bases in 3D
        for base in bases:
            if player_grid_x == base['x'] and player_grid_y == base['y']:
                # More complex base shape
                size = 50
                pygame.draw.rect(screen, BLUE, (x - size, y - size, size*2, size*2))
                pygame.draw.rect(screen, WHITE, (x - size/2, y - size/2, size, size))
                pygame.draw.line(screen, GREEN, (x, y - size * 1.5), (x, y + size * 1.5), 5)
                pygame.draw.line(screen, GREEN, (x - size * 1.5, y), (x + size * 1.5, y), 5)

        # Draw Planets in 3D
        for p in planets:
            if player_grid_x == p['x'] and player_grid_y == p['y']:
                planet_z = 200
                k = 128.0 / planet_z
                x = int(0 * k + SCREEN_WIDTH / 2)
                y = int(0 * k + SCREEN_HEIGHT / 2)
                size = 30
                if p['has_key']:
                    pygame.draw.circle(screen, YELLOW, (x, y), size)
                else:
                    pygame.draw.circle(screen, (100, 100, 255), (x, y), size)

        # Draw Asteroids
        for asteroid in asteroids:
            k = 128.0 / asteroid['z'] if asteroid['z'] != 0 else 128.0
            x = int(asteroid['x'] * k + SCREEN_WIDTH / 2)
            y = int(asteroid['y'] * k + SCREEN_HEIGHT / 2)

            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                size = (1 - asteroid['z'] / SCREEN_WIDTH) * asteroid['size']
                pygame.draw.circle(screen, (128, 128, 128), (x, y), size)


        # Draw Enemies
        for enemy in enemies:
            k = 128.0 / enemy['z'] if enemy['z'] != 0 else 128.0
            x = int(enemy['x'] * k + SCREEN_WIDTH / 2)
            y = int(enemy['y'] * k + SCREEN_HEIGHT / 2)

            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                size = (1 - enemy['z'] / SCREEN_WIDTH) * 20
                if enemy['type'] == 'fighter':
                    # T-shape fighter
                    points = [
                        (x - size, y - size / 3),
                        (x + size, y - size / 3),
                        (x + size, y + size / 3),
                        (x - size, y + size / 3),
                    ]
                    pygame.draw.polygon(screen, RED, points, 1)
                    pygame.draw.line(screen, RED, (x, y - size / 3), (x, y + size), 1)
                elif enemy['type'] == 'bomber':
                    # Wide bomber
                    points = [
                        (x - size * 1.5, y - size / 2),
                        (x + size * 1.5, y - size / 2),
                        (x + size, y + size / 2),
                        (x - size, y + size / 2),
                    ]
                    pygame.draw.polygon(screen, ORANGE, points, 1)
                elif enemy['type'] == 'cruiser':
                    # Cruiser with wings
                    points = [
                        (x, y - size),
                        (x - size * 2, y + size),
                        (x + size * 2, y + size),
                    ]
                    pygame.draw.polygon(screen, (200, 200, 200), points, 1)
                    pygame.draw.line(screen, (200, 200, 200), (x, y - size), (x, y + size), 1)
                elif enemy['type'] == 'boss':
                    # More complex boss
                    pygame.draw.rect(screen, MAGENTA, (x - size, y - size, size * 2, size * 2), 1)
                    pygame.draw.line(screen, MAGENTA, (x - size, y - size), (x + size, y + size), 1)
                    pygame.draw.line(screen, MAGENTA, (x + size, y - size), (x - size, y + size), 1)



        # Draw Bullets
        for bullet in bullets:
            k = 128.0 / bullet['z'] if bullet['z'] != 0 else 128.0
            x = int(bullet['x'] * k + SCREEN_WIDTH / 2)
            y = int(bullet['y'] * k + SCREEN_HEIGHT / 2)

            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                start_pos = (x, y)
                end_pos = (x, y - 10)
                pygame.draw.line(screen, YELLOW, start_pos, end_pos, 2)


        # Draw Missiles
        for missile in missiles:
            k = 128.0 / missile['z'] if missile['z'] != 0 else 128.0
            x = int(missile['x'] * k + SCREEN_WIDTH / 2)
            y = int(missile['y'] * k + SCREEN_HEIGHT / 2)

            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                pygame.draw.rect(screen, CYAN, (x-2, y-5, 4, 10), 1)

        # Draw Enemy Bullets
        for bullet in enemy_bullets:
            k = 128.0 / bullet['z'] if bullet['z'] != 0 else 128.0
            x = int(bullet['x'] * k + SCREEN_WIDTH / 2)
            y = int(bullet['y'] * k + SCREEN_HEIGHT / 2)

            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                start_pos = (x, y)
                end_pos = (x, y + 5)
                pygame.draw.line(screen, RED, start_pos, end_pos, 2)
        
        # Draw Explosions
        for explosion in explosions:
            k = 128.0 / explosion['z'] if explosion['z'] != 0 else 128.0
            x = int(explosion['x'] * k + SCREEN_WIDTH / 2)
            y = int(explosion['y'] * k + SCREEN_HEIGHT / 2)
            
            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                pygame.draw.circle(screen, ORANGE, (x, y), explosion['radius'], 1)

        # Draw damage effect
        if damage_effect > 0:
            damage_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            damage_surface.fill((255, 0, 0, 128))
            screen.blit(damage_surface, (0, 0))
            damage_effect -= 1

        # Update and Draw Shield Hit Particles



        # Draw Cockpit
        draw_cockpit_frame()
        draw_hud()
        draw_radar()
    elif game_state == 'map':
        draw_star_map()
    
    elif game_state == 'won':
        font = pygame.font.Font(None, 100)
        text = font.render("YOU WIN!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)
    
    elif game_state == 'lost':
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        font = pygame.font.Font(None, 100)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 50)
        score_text = font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(score_text, score_rect)

        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        screen.blit(high_score_text, high_score_rect)

        restart_text = font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100))
        screen.blit(restart_text, restart_rect)

    elif game_state == 'menu':
        screen.fill(BLACK)
        font = pygame.font.Font(None, 100)
        text = font.render("STAR SHOOTER", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 50)
        adventure_text = font.render("1. Adventure Mode", True, WHITE)
        adventure_rect = adventure_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        screen.blit(adventure_text, adventure_rect)

        command_text = font.render("2. Command Mode", True, WHITE)
        command_rect = command_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(command_text, command_rect)

        training_text = font.render("3. Training Mode", True, WHITE)
        training_rect = training_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        screen.blit(training_text, training_rect)

        # Handle menu input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_state = 'playing'
                    reset_game(mode='adventure')
                elif event.key == pygame.K_2:
                    game_state = 'playing' # Start playing after mode selection
                    reset_game(mode='command')
                elif event.key == pygame.K_3:
                    game_state = 'playing' # Start playing after mode selection
                    reset_game(mode='training')


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()