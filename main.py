import pygame
import random
import math
import os

def handle_high_scores(score):
    high_scores = []
    try:
        with open("highscore.txt", "r") as f:
            high_scores = [int(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        pass

    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:10] # Keep only the top 10 scores

    with open("highscore.txt", "w") as f:
        for s in high_scores:
            f.write(str(s) + "\n")

    return high_scores



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
player_fuel = 1000
MAX_FUEL = 1500
player_shields = 100
MAX_SHIELDS = 150
player_missiles = 5
ship_systems = {'radar': 100, 'computer': 100, 'engine': 100}
score = 0
high_score = 0

# Planets
planets = []
keys_collected_count = 0
boss = None

# Game State
game_state = 'title' # title, playing, won, lost, map, menu
warp_targeting = False
target_grid_x = player_grid_x
target_grid_y = player_grid_y
date = 0
MAX_DATE = 1500
asteroid_fields = []
asteroids = []
shield_hit_particles = []
target_cursor_x = 0
target_cursor_y = 0

# Grid
GRID_SIZE = 8
sector_types = [['empty' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

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
enemy_type = random.choice(['batte', 'gol', 'demo'])
health = {'batte': 7, 'gol': 15, 'demo': 30}[enemy_type]
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
    global player_angle, player_rotation_speed, player_speed, player_grid_x, player_grid_y, player_fuel, player_shields, player_missiles, game_state, warp_targeting, target_grid_x, target_grid_y, stars, bullets, missiles, explosions, enemy_bullets, enemies, bases, score, planets, keys_collected_count, boss, date, target_cursor_x, target_cursor_y, asteroid_fields, asteroids, shield_hit_particles, ship_systems, sector_types, high_score
    player_angle = 0
    player_rotation_speed = 0
    player_speed = 0
    player_grid_x = 4
    player_grid_y = 4
    player_fuel = 1500
    player_shields = 150
    player_missiles = 10
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
    bases.append({'x': 7, 'y': 7, 'health': 100})
    planets = []
    keys_collected_count = 0
    boss = None
    date = 0
    asteroid_fields = []
    shield_hit_particles = []
    sector_types = [['empty' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.readline().strip())
    except (FileNotFoundError, ValueError):
        high_score = 0

    # Generate nebulas
    for _ in range(3):
        nx = random.randint(0, GRID_SIZE - 1)
        ny = random.randint(0, GRID_SIZE - 1)
        sector_types[nx][ny] = 'nebula'

    # Generate asteroid fields
    for _ in range(5):
        ax = random.randint(0, GRID_SIZE - 1)
        ay = random.randint(0, GRID_SIZE - 1)
        if sector_types[ax][ay] == 'empty':
            sector_types[ax][ay] = 'asteroid_field'

    if mode == 'adventure':
        # Create 3 planets with keys
        while len(planets) < 3:
            planet_x = random.randint(0, GRID_SIZE - 1)
            planet_y = random.randint(0, GRID_SIZE - 1)
            is_on_base = any(base['x'] == planet_x and base['y'] == planet_y for base in bases)
            is_on_player_start = (planet_x == 4 and planet_y == 4)
            is_duplicate = any(p['x'] == planet_x and p['y'] == planet_y for p in planets)
            if not is_on_base and not is_on_player_start and not is_duplicate:
                planets.append({'x': planet_x, 'y': planet_y, 'has_key': True})

        # Create some more planets without keys
        while len(planets) < 7:
            planet_x = random.randint(0, GRID_SIZE - 1)
            planet_y = random.randint(0, GRID_SIZE - 1)
            is_on_base = any(base['x'] == planet_x and base['y'] == planet_y for base in bases)
            is_on_player_start = (planet_x == 4 and planet_y == 4)
            is_duplicate = any(p['x'] == planet_x and p['y'] == planet_y for p in planets)
            if not is_on_base and not is_on_player_start and not is_duplicate:
                planets.append({'x': planet_x, 'y': planet_y, 'has_key': False})
        enemy_type = random.choice(['batte', 'gol', 'demo'])
        health = {'batte': 7, 'gol': 15, 'demo': 30}[enemy_type]
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
            enemy_type = random.choice(['batte', 'gol', 'demo'])
            health = {'batte': 7, 'gol': 15, 'demo': 30}[enemy_type]
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
            enemy_type = random.choice(['batte', 'demo']) # No gols in training
            health = {'batte': 7, 'gol': 15, 'demo': 30}[enemy_type]
            enemies.append({'x': random.randint(-100, 100), 'y': random.randint(-100, 100), 'z': random.randint(200, 500), 'type': enemy_type, 'grid_x': random.randint(0, GRID_SIZE - 1), 'grid_y': random.randint(0, GRID_SIZE - 1), 'health': health})
        # No keys, no boss, no bases, no asteroid fields in training mode
        planets = []
        keys_collected_count = 0
        boss = None
        bases = []
        asteroid_fields = []

def draw_title_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text = font.render("STAR SHOOTER", True, YELLOW)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 50)
    text = font.render("Press any key to start", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect)

def draw_star_map():
    screen.fill(BLACK)
    
    cell_width = SCREEN_WIDTH / GRID_SIZE
    cell_height = SCREEN_HEIGHT / GRID_SIZE
    font = pygame.font.Font(None, 24)
    symbol_font = pygame.font.Font(None, 32)

    # Draw grid with authentic Star Luster style
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_x = x * cell_width
            cell_y = y * cell_height
            
            # Background for special sectors
            if sector_types[x][y] == 'nebula':
                pygame.draw.rect(screen, (30, 30, 60), (cell_x, cell_y, cell_width, cell_height))
            elif sector_types[x][y] == 'asteroid_field':
                pygame.draw.rect(screen, (60, 60, 60), (cell_x, cell_y, cell_width, cell_height))
            
            # Grid lines
            pygame.draw.rect(screen, GREEN, (cell_x, cell_y, cell_width, cell_height), 1)

    # Draw bases with authentic "B" symbol
    for base in bases:
        base_map_x = base['x'] * cell_width + cell_width / 2
        base_map_y = base['y'] * cell_height + cell_height / 2
        health_ratio = base['health'] / 100.0
        if health_ratio > 0.5:
            color = BLUE
        elif health_ratio > 0.2:
            color = YELLOW
        else:
            color = RED
        # Draw "B" symbol
        b_text = symbol_font.render("B", True, color)
        b_rect = b_text.get_rect(center=(base_map_x, base_map_y))
        screen.blit(b_text, b_rect)

    # Draw planets with authentic "*" symbol
    for p in planets:
        planet_map_x = p['x'] * cell_width + cell_width / 2
        planet_map_y = p['y'] * cell_height + cell_height / 2
        if p.get('has_key'):
            # Yellow star for planets with keys
            star_text = symbol_font.render("*", True, YELLOW)
        elif p.get('is_final'):
            # Magenta star for final planet
            star_text = symbol_font.render("*", True, MAGENTA)
        else:
            # White star for regular planets
            star_text = symbol_font.render("*", True, WHITE)
        star_rect = star_text.get_rect(center=(planet_map_x, planet_map_y))
        screen.blit(star_text, star_rect)

    # Draw asteroid fields with "::" symbol
    for af in asteroid_fields:
        af_map_x = af['x'] * cell_width + cell_width / 2
        af_map_y = af['y'] * cell_height + cell_height / 2
        af_text = font.render("::", True, (150, 150, 150))
        af_rect = af_text.get_rect(center=(af_map_x, af_map_y))
        screen.blit(af_text, af_rect)

    # Count enemies per sector and draw "E" with count
    enemy_counts = {}
    for enemy in enemies:
        key = (enemy['grid_x'], enemy['grid_y'])
        enemy_counts[key] = enemy_counts.get(key, 0) + 1
    
    for (ex, ey), count in enemy_counts.items():
        enemy_map_x = ex * cell_width + cell_width / 2
        enemy_map_y = ey * cell_height + cell_height / 2
        # Check if it's the boss
        is_boss = any(e['type'] in ['boss', 'battsura'] and e['grid_x'] == ex and e['grid_y'] == ey for e in enemies)
        color = MAGENTA if is_boss else RED
        e_text = symbol_font.render("E", True, color)
        e_rect = e_text.get_rect(center=(enemy_map_x, enemy_map_y - 5))
        screen.blit(e_text, e_rect)
        # Show count if more than 1
        if count > 1:
            count_text = font.render(str(count), True, color)
            count_rect = count_text.get_rect(center=(enemy_map_x, enemy_map_y + 10))
            screen.blit(count_text, count_rect)

    # Draw player with heading indicator
    player_map_x = player_grid_x * cell_width + cell_width / 2
    player_map_y = player_grid_y * cell_height + cell_height / 2
    pygame.draw.circle(screen, YELLOW, (player_map_x, player_map_y), 6)
    pygame.draw.circle(screen, YELLOW, (player_map_x, player_map_y), 3)
    # Heading line
    heading_x = player_map_x + 25 * math.sin(math.radians(player_angle))
    heading_y = player_map_y - 25 * math.cos(math.radians(player_angle))
    pygame.draw.line(screen, YELLOW, (player_map_x, player_map_y), (heading_x, heading_y), 2)

    # Draw cursor (targeting)
    cursor_x = target_cursor_x * cell_width
    cursor_y = target_cursor_y * cell_height
    pygame.draw.rect(screen, WHITE, (cursor_x, cursor_y, cell_width, cell_height), 3)
    # Cursor corners
    corner_size = 10
    pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x + corner_size, cursor_y), 3)
    pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + corner_size), 3)
    pygame.draw.line(screen, WHITE, (cursor_x + cell_width, cursor_y), (cursor_x + cell_width - corner_size, cursor_y), 3)
    pygame.draw.line(screen, WHITE, (cursor_x + cell_width, cursor_y), (cursor_x + cell_width, cursor_y + corner_size), 3)
    
    # Map title and instructions
    title_text = font.render("GALACTIC MAP", True, GREEN)
    screen.blit(title_text, (10, 10))
    inst_text = font.render("ARROWS:Move  SPACE:Photon Torpedo  M:Exit", True, WHITE)
    screen.blit(inst_text, (10, SCREEN_HEIGHT - 20))


def draw_cockpit_frame():
    # Authentic Star Luster-style cockpit with green wireframe aesthetic
    cockpit_color = (0, 80, 0) # Dark green background
    cockpit_bright = (0, 200, 0) # Bright green for wireframe
    
    # Top and bottom bars
    pygame.draw.rect(screen, cockpit_color, (0, 0, SCREEN_WIDTH, 100))
    pygame.draw.rect(screen, cockpit_color, (0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150))
    # Side bars
    pygame.draw.rect(screen, cockpit_color, (0, 100, 100, SCREEN_HEIGHT - 250))
    pygame.draw.rect(screen, cockpit_color, (SCREEN_WIDTH - 100, 100, 100, SCREEN_HEIGHT - 250))
    
    # Main viewport outline with double border for depth
    pygame.draw.rect(screen, GREEN, (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 250), 3)
    pygame.draw.rect(screen, cockpit_bright, (105, 105, SCREEN_WIDTH - 210, SCREEN_HEIGHT - 260), 1)

    # Corner brackets (authentic Star Luster style)
    bracket_size = 25
    # Top-left
    pygame.draw.line(screen, cockpit_bright, (100, 100), (100 + bracket_size, 100), 3)
    pygame.draw.line(screen, cockpit_bright, (100, 100), (100, 100 + bracket_size), 3)
    # Top-right
    pygame.draw.line(screen, cockpit_bright, (SCREEN_WIDTH - 100, 100), (SCREEN_WIDTH - 100 - bracket_size, 100), 3)
    pygame.draw.line(screen, cockpit_bright, (SCREEN_WIDTH - 100, 100), (SCREEN_WIDTH - 100, 100 + bracket_size), 3)
    # Bottom-left
    pygame.draw.line(screen, cockpit_bright, (100, SCREEN_HEIGHT - 150), (100 + bracket_size, SCREEN_HEIGHT - 150), 3)
    pygame.draw.line(screen, cockpit_bright, (100, SCREEN_HEIGHT - 150), (100, SCREEN_HEIGHT - 150 - bracket_size), 3)
    # Bottom-right
    pygame.draw.line(screen, cockpit_bright, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150), (SCREEN_WIDTH - 100 - bracket_size, SCREEN_HEIGHT - 150), 3)
    pygame.draw.line(screen, cockpit_bright, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150 - bracket_size), 3)
    
    # Instrumentation panels (decorative lines)
    # Left panel details
    for i in range(3):
        y_pos = 120 + i * 30
        pygame.draw.line(screen, GREEN, (10, y_pos), (90, y_pos), 1)
    # Right panel details
    for i in range(3):
        y_pos = 120 + i * 30
        pygame.draw.line(screen, GREEN, (SCREEN_WIDTH - 90, y_pos), (SCREEN_WIDTH - 10, y_pos), 1)
    # Bottom panel grid
    for i in range(5):
        x_pos = 150 + i * 100
        pygame.draw.line(screen, GREEN, (x_pos, SCREEN_HEIGHT - 140), (x_pos, SCREEN_HEIGHT - 10), 1)

def draw_hud():
    font = pygame.font.Font(None, 30)
    small_font = pygame.font.Font(None, 20)
    
    # --- Top Center ---
    # Score
    score_text = font.render(f"SCORE: {score}", True, GREEN)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, 25))
    screen.blit(score_text, score_rect)
    # High Score
    high_score_text = small_font.render(f"HIGH: {high_score}", True, YELLOW)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH/2, 50))
    screen.blit(high_score_text, high_score_rect)

    # --- Bottom Left ---
    # Fuel Gauge (as an arc)
    fuel_angle = (player_fuel / MAX_FUEL) * 180
    pygame.draw.arc(screen, GREEN, (10, SCREEN_HEIGHT - 140, 80, 80), math.radians(180), math.radians(180 + fuel_angle), 5)
    fuel_text = small_font.render("FUEL", True, GREEN)
    screen.blit(fuel_text, (25, SCREEN_HEIGHT - 125))
    fuel_value = small_font.render(f"{int(player_fuel)}", True, WHITE)
    screen.blit(fuel_value, (25, SCREEN_HEIGHT - 105))

    # Shield Gauge (as an arc)
    shield_angle = (player_shields / MAX_SHIELDS) * 180
    shield_color = GREEN if player_shields > 50 else (YELLOW if player_shields > 20 else RED)
    pygame.draw.arc(screen, shield_color, (10, SCREEN_HEIGHT - 90, 80, 80), math.radians(180), math.radians(180 + shield_angle), 5)
    shield_text = small_font.render("SHIELD", True, shield_color)
    screen.blit(shield_text, (20, SCREEN_HEIGHT - 75))
    shield_value = small_font.render(f"{int(player_shields)}", True, WHITE)
    screen.blit(shield_value, (30, SCREEN_HEIGHT - 55))

    # --- Bottom Right ---
    # Missile Count (as vertical bars)
    missile_text = small_font.render("MISSILES", True, GREEN)
    screen.blit(missile_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 130))
    for i in range(min(player_missiles, 10)):  # Show max 10 bars
        pygame.draw.rect(screen, CYAN, (SCREEN_WIDTH - 90 + (i * 8), SCREEN_HEIGHT - 110, 6, 25))
    if player_missiles > 10:
        extra_text = small_font.render(f"+{player_missiles - 10}", True, CYAN)
        screen.blit(extra_text, (SCREEN_WIDTH - 90, SCREEN_HEIGHT - 80))

    # --- Bottom Center ---
    # Date
    date_text = small_font.render(f"DATE: {date:04d}", True, GREEN)
    date_rect = date_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 20))
    screen.blit(date_text, date_rect)
    # Keys
    key_text = font.render(f"KEYS: {keys_collected_count}/3", True, YELLOW)
    key_rect = key_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 45))
    screen.blit(key_text, key_rect)

    # --- Left Side ---
    # System Status (Enhanced with bars)
    system_font = pygame.font.Font(None, 22)
    system_names = {'radar': 'RAD', 'computer': 'COM', 'engine': 'ENG'}
    for i, (system, health) in enumerate(ship_systems.items()):
        y_pos = 110 + i * 30
        # System name
        color = GREEN if health > 50 else (YELLOW if health > 20 else RED)
        text = system_font.render(f"{system_names[system]}", True, color)
        screen.blit(text, (10, y_pos))
        # Health bar
        bar_width = 60
        bar_height = 8
        pygame.draw.rect(screen, (50, 50, 50), (50, y_pos + 5, bar_width, bar_height))
        pygame.draw.rect(screen, color, (50, y_pos + 5, int(bar_width * health / 100), bar_height))
        # Percentage
        percent_text = small_font.render(f"{int(health)}%", True, color)
        screen.blit(percent_text, (115, y_pos + 2))

    # --- Targeting Computer (Right Side) ---
    # Find nearest enemy for targeting
    nearest_enemy = None
    min_dist = float('inf')
    for enemy in enemies:
        if enemy['grid_x'] == player_grid_x and enemy['grid_y'] == player_grid_y:
            dist = math.sqrt(enemy['x']**2 + enemy['y']**2 + enemy['z']**2)
            if dist < min_dist:
                min_dist = dist
                nearest_enemy = enemy
    
    if nearest_enemy and ship_systems['computer'] > 0:
        target_font = pygame.font.Font(None, 20)
        enemy_type_names = {'batte': 'BATTE', 'gol': 'GOL', 'demo': 'DEMO', 'battsura': 'BATTSURA', 'boss': 'BATTSURA'}
        enemy_name = enemy_type_names.get(nearest_enemy['type'], 'ENEMY')
        target_text = target_font.render(f"TGT: {enemy_name}", True, RED)
        screen.blit(target_text, (SCREEN_WIDTH - 100, 110))
        dist_text = target_font.render(f"DST: {int(min_dist)}", True, RED)
        screen.blit(dist_text, (SCREEN_WIDTH - 100, 130))
        # Lock indicator
        if min_dist < 300:
            lock_text = target_font.render("LOCK", True, YELLOW)
            screen.blit(lock_text, (SCREEN_WIDTH - 100, 150))

def draw_radar():
    radar_x = SCREEN_WIDTH / 2
    radar_y = SCREEN_HEIGHT - 75
    radar_radius = 65
    
    # Radar background
    pygame.draw.circle(screen, (0, 40, 0), (radar_x, radar_y), radar_radius)
    
    if ship_systems['radar'] == 0:
        # Radar is completely out
        font = pygame.font.Font(None, 20)
        text = font.render("RADAR OUT", True, RED)
        text_rect = text.get_rect(center=(radar_x, radar_y))
        screen.blit(text, text_rect)
        return

    # Radar grid circles
    pygame.draw.circle(screen, GREEN, (radar_x, radar_y), radar_radius, 2)
    pygame.draw.circle(screen, GREEN, (radar_x, radar_y), radar_radius * 2/3, 1)
    pygame.draw.circle(screen, GREEN, (radar_x, radar_y), radar_radius / 3, 1)
    # Crosshairs
    pygame.draw.line(screen, GREEN, (radar_x - radar_radius, radar_y), (radar_x + radar_radius, radar_y), 1)
    pygame.draw.line(screen, GREEN, (radar_x, radar_y - radar_radius), (radar_x, radar_y + radar_radius), 1)

    # Radar sweep line
    sweep_angle = (pygame.time.get_ticks() % 2000) / 2000 * 360
    sweep_end_x = radar_x + radar_radius * 0.9 * math.cos(math.radians(sweep_angle - 90))
    sweep_end_y = radar_y + radar_radius * 0.9 * math.sin(math.radians(sweep_angle - 90))
    pygame.draw.line(screen, (0, 255, 0), (radar_x, radar_y), (sweep_end_x, sweep_end_y), 1)

    # Player in center (yellow triangle pointing up)
    player_points = [
        (radar_x, radar_y - 5),
        (radar_x - 3, radar_y + 3),
        (radar_x + 3, radar_y + 3)
    ]
    pygame.draw.polygon(screen, YELLOW, player_points)

    # Draw objects on radar
    if ship_systems['radar'] < 20:
        # Severely damaged - only player visible
        return

    # Flickering effect when damaged
    if ship_systems['radar'] < 50 and random.random() < 0.5:
        return

    # Show bases in current sector
    for base in bases:
        if base['x'] == player_grid_x and base['y'] == player_grid_y:
            # Base is in current sector - show at edge
            pygame.draw.rect(screen, BLUE, (radar_x - 4, radar_y - radar_radius + 5, 8, 8))

    # Show planets in current sector
    for planet in planets:
        if planet['x'] == player_grid_x and planet['y'] == player_grid_y:
            # Planet in sector - show at edge
            planet_color = YELLOW if planet.get('has_key') else (150, 150, 255)
            pygame.draw.circle(screen, planet_color, (radar_x + radar_radius - 10, radar_y), 4)

    # Enemies with type-specific indicators
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
            if radar_dist < 600: # Show enemies within range
                angle = math.atan2(rotated_x, -rotated_z)
                display_dist = min((radar_dist / 600) * radar_radius * 0.9, radar_radius * 0.9)
                
                blip_x = radar_x + display_dist * math.sin(angle)
                blip_y = radar_y + display_dist * math.cos(angle)
                
                # Different shapes for different enemy types
                if enemy['type'] == 'batte':
                    # Small red dot for fighters
                    pygame.draw.circle(screen, RED, (blip_x, blip_y), 2)
                elif enemy['type'] == 'gol':
                    # Orange square for Gols
                    pygame.draw.rect(screen, ORANGE, (blip_x - 2, blip_y - 2, 4, 4))
                elif enemy['type'] == 'demo':
                    # Gray triangle for Demos
                    pygame.draw.polygon(screen, (200, 200, 200), [
                        (blip_x, blip_y - 3),
                        (blip_x - 3, blip_y + 2),
                        (blip_x + 3, blip_y + 2)
                    ])
                elif enemy['type'] in ['boss', 'battsura']:
                    # Large magenta circle for boss
                    pygame.draw.circle(screen, MAGENTA, (blip_x, blip_y), 5)
                    pygame.draw.circle(screen, MAGENTA, (blip_x, blip_y), 3, 1)

    # Target Reticle (enhanced)
    reticle_size = 15
    reticle_color = GREEN if ship_systems['computer'] > 0 else RED
    pygame.draw.line(screen, reticle_color, (SCREEN_WIDTH/2 - reticle_size, SCREEN_HEIGHT/2), (SCREEN_WIDTH/2 + reticle_size, SCREEN_HEIGHT/2), 2)
    pygame.draw.line(screen, reticle_color, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - reticle_size), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + reticle_size), 2)
    pygame.draw.circle(screen, reticle_color, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 8, 1)


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
        if game_state == 'title':
            if event.type == pygame.KEYDOWN:
                game_state = 'menu'
        elif game_state == 'playing':
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
                            fuel_cost = int(dist * 10)
                            if player_fuel >= fuel_cost:
                                if warp_sound: warp_sound.play()
                                player_fuel -= fuel_cost
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
                                enemy_type = random.choice(['batte', 'gol', 'demo'])
                                health = {'batte': 10, 'gol': 20, 'demo': 50}[enemy_type]
                                enemies.append({'x': random.randint(-100, 100), 'y': random.randint(-100, 100), 'z': 500, 'type': enemy_type, 'grid_x': target_grid_x, 'grid_y': target_grid_y, 'health': health})
                if event.key == pygame.K_SPACE:
                    if player_shields >= 1:
                        if laser_sound: laser_sound.play()
                        player_shields -= 1
                        bullets.append({'x': 0, 'y': 0, 'z': 0, 'vx': 0, 'vy': 0, 'vz': 40})
                if event.key == pygame.K_n:
                    if player_missiles > 0:
                        if missile_sound: missile_sound.play()
                        player_missiles -= 1
                        missiles.append({'x': 0, 'y': 0, 'z': 0, 'vx': 0, 'vy': 0, 'vz': 10})
                if event.key == pygame.K_m:
                    game_state = 'map'
                if event.key == pygame.K_h:
                    if ship_systems['computer'] > 0 and player_fuel >= 50:
                        if warp_sound: warp_sound.play()
                        player_fuel -= 50
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

        if sector_types[player_grid_x][player_grid_y] == 'nebula':
            engine_efficiency *= 0.5 # Reduce speed in nebula

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

        if sector_types[player_grid_x][player_grid_y] == 'asteroid_field':
            if random.random() < 0.1:
                if shield_hit_sound: shield_hit_sound.play()
                if random.random() < 0.2: # 20% chance to damage a system
                    system_to_damage = random.choice(list(ship_systems.keys()))
                    ship_systems[system_to_damage] -= 10 # Asteroids do more damage
                    if ship_systems[system_to_damage] < 0:
                        ship_systems[system_to_damage] = 0
                else:
                    player_shields -= 10
                damage_effect = 10 # Red overlay



        # Update bullets and missiles
        for projectile in bullets + missiles:
            projectile['x'] += projectile['vx']
            projectile['y'] += projectile['vy']
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
            elif enemy['type'] == 'batte':
                if enemy['z'] > 200:
                    enemy['z'] -= 2
                else:
                    if enemy['x'] < 0:
                        enemy['x'] -= 1
                    else:
                        enemy['x'] += 1
                # Fighters shoot at the player
                if random.random() < 0.02:
                    enemy_bullets.append({'x': enemy['x'], 'y': enemy['y'], 'z': enemy['z'], 'vx': 0, 'vy': 0, 'vz': -10})
            elif enemy['type'] == 'gol':
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
            elif enemy['type'] == 'demo':
                enemy['z'] -= 0.1 # Cruisers are slow
                # Cruisers shoot powerful shots less frequently
                if random.random() < 0.01:
                    enemy_bullets.append({'x': enemy['x'], 'y': enemy['y'], 'z': enemy['z'], 'vx': 0, 'vy': 0, 'vz': -5, 'power': 20}) # More power

            if enemy['z'] < 0:
                if enemy in enemies: 
                    if shield_hit_sound: shield_hit_sound.play()
                    enemies.remove(enemy)
                    player_shields -= 10
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
                        if enemy['type'] == 'battsura':
                            if win_sound: win_sound.play()
                            game_state = 'won'
                            score += 1000
                        elif enemy['type'] == 'batte':
                            score += 10
                        elif enemy['type'] == 'gol':
                            score += 20
                        elif enemy['type'] == 'demo':
                            score += 50
                        enemies.remove(enemy)

                        # Check if all enemies in the sector are destroyed
                        sector_enemies = [e for e in enemies if e['grid_x'] == player_grid_x and e['grid_y'] == player_grid_y]
                        if not sector_enemies:
                            score += 100 # Bonus for clearing the sector

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
                if random.random() < 0.2: # 20% chance to damage a system
                    system_to_damage = random.choice(list(ship_systems.keys()))
                    ship_systems[system_to_damage] -= 10
                    if ship_systems[system_to_damage] < 0:
                        ship_systems[system_to_damage] = 0
                else:
                    player_shields -= bullet.get('power', 5)
                damage_effect = 10 # Red overlay

        # Asteroid Collision
        for asteroid in asteroids:
            dist = math.sqrt(asteroid['x']**2 + asteroid['y']**2 + asteroid['z']**2)
            if dist < asteroid['size']:
                if shield_hit_sound: shield_hit_sound.play()
                if random.random() < 0.2: # 20% chance to damage a system
                    system_to_damage = random.choice(list(ship_systems.keys()))
                    ship_systems[system_to_damage] -= 20 # Asteroids do more damage
                    if ship_systems[system_to_damage] < 0:
                        ship_systems[system_to_damage] = 0
                else:
                    player_shields -= 10
                damage_effect = 10 # Red overlay
                asteroids.remove(asteroid)

        
        # Docking and refueling
        for base in bases:
            if player_grid_x == base['x'] and player_grid_y == base['y']:
                player_fuel += 10
                if player_fuel > MAX_FUEL:
                    player_fuel = MAX_FUEL
                player_shields += 2
                if player_shields > MAX_SHIELDS:
                    player_shields = MAX_SHIELDS
                player_missiles = 5 # Refill missiles at base
                # Repair systems
                for system in ship_systems:
                    if ship_systems[system] < 100:
                        ship_systems[system] += 0.5
                        if ship_systems[system] > 100:
                            ship_systems[system] = 100



        # Check for game over
        if player_fuel <= 0 or player_shields <= 0 or date >= MAX_DATE:
            if game_over_sound: game_over_sound.play()
            game_state = 'lost'

        # Key Collection from planets
        for p in planets:
            if player_grid_x == p['x'] and player_grid_y == p['y'] and p['has_key']:
                p['has_key'] = False
                keys_collected_count += 1
                # Spawn boss if all keys are collected
                if keys_collected_count == 3:
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
                if enemy['type'] == 'batte':
                    # T-shape fighter
                    points = [
                        (x - size, y - size / 3),
                        (x + size, y - size / 3),
                        (x + size, y + size / 3),
                        (x - size, y + size / 3),
                    ]
                    pygame.draw.polygon(screen, RED, points, 1)
                    pygame.draw.line(screen, RED, (x, y - size / 3), (x, y + size), 1)
                elif enemy['type'] == 'gol':
                    points = [
                        (x - size * 1.5, y - size / 2),
                        (x + size * 1.5, y - size / 2),
                        (x + size, y + size / 2),
                        (x - size, y + size / 2),
                    ]
                    pygame.draw.polygon(screen, ORANGE, points, 1)
                elif enemy['type'] == 'demo':
                    # Cruiser with wings
                    points = [
                        (x, y - size),
                        (x - size * 2, y + size),
                        (x + size * 2, y + size),
                    ]
                    pygame.draw.polygon(screen, (200, 200, 200), points, 1)
                    pygame.draw.line(screen, (200, 200, 200), (x, y - size), (x, y + size), 1)
                elif enemy['type'] == 'battsura':
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
        if date < 500:
            score += (500 - date) * 10 # Time bonus
        font = pygame.font.Font(None, 100)
        text = font.render("YOU WIN!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)
    
    elif game_state == 'lost':
        high_scores = handle_high_scores(score)

        font = pygame.font.Font(None, 100)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 50)
        score_text = font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        screen.blit(score_text, score_rect)

        high_score_title_text = font.render("High Scores", True, YELLOW)
        high_score_title_rect = high_score_title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        screen.blit(high_score_title_text, high_score_title_rect)

        for i, high_score in enumerate(high_scores):
            high_score_text = font.render(f"{i+1}. {high_score}", True, WHITE)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + i * 40))
            screen.blit(high_score_text, high_score_rect)

        restart_text = font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + len(high_scores) * 40 + 50))
        screen.blit(restart_text, restart_rect)
    
    elif game_state == 'title':
        draw_title_screen()

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
