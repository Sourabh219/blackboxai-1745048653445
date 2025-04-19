import pygame
import random
import sys

# Initialize Pygame and mixer for sounds
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
YELLOW = (255, 255, 0)

# Player settings
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Bullet settings
bullets = []
bullet_speed = 10
bullet_radius = 5
bullet_cooldown = 10  # frames
bullet_timer = 0

# Enemy settings
enemy_size = 40
enemies = []
enemy_speed = 2
spawn_delay = 30  # frames
frame_count = 0

# Explosion settings
explosions = []
explosion_duration = 15  # frames

# Game state
score = 0
game_over = False

# Fonts
font = pygame.font.SysFont("Arial", 24)
game_over_font = pygame.font.SysFont("Arial", 64)

# Sounds (simple beep sounds)
shoot_sound = pygame.mixer.Sound(pygame.mixer.Sound.buffer(b'\x00'*1000))
hit_sound = pygame.mixer.Sound(pygame.mixer.Sound.buffer(b'\x00'*1000))

def play_shoot_sound():
    # Simple beep for shooting
    frequency = 440
    duration = 100
    pygame.mixer.Sound.play(shoot_sound)

def play_hit_sound():
    # Simple beep for hit
    frequency = 220
    duration = 100
    pygame.mixer.Sound.play(hit_sound)

def draw_player(x, y):
    # Draw a simple plane shape using polygons
    # Triangle nose
    pygame.draw.polygon(win, BLACK, [(x + player_size//2, y), (x + player_size//4, y + player_size//2), (x + 3*player_size//4, y + player_size//2)])
    # Rectangle body
    pygame.draw.rect(win, BLACK, (x + player_size//4, y + player_size//2, player_size//2, player_size//3))
    # Wings
    pygame.draw.polygon(win, BLACK, [(x, y + player_size//2), (x + player_size//4, y + player_size//2), (x, y + player_size)])
    pygame.draw.polygon(win, BLACK, [(x + player_size, y + player_size//2), (x + 3*player_size//4, y + player_size//2), (x + player_size, y + player_size)])

def draw_explosions():
    for exp in explosions[:]:
        x, y, timer = exp
        pygame.draw.circle(win, YELLOW, (x, y), 20 * (timer / explosion_duration))
        timer -= 1
        if timer <= 0:
            explosions.remove(exp)
        else:
            explosions[explosions.index(exp)] = (x, y, timer)

def reset_game():
    global bullets, enemies, explosions, score, game_over, player_x, bullet_timer, frame_count
    bullets = []
    enemies = []
    explosions = []
    score = 0
    game_over = False
    player_x = WIDTH // 2
    bullet_timer = 0
    frame_count = 0

# Main loop
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(60)
    win.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player movement
        if keys[pygame.K_LEFT] and player_x - player_speed > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_speed < WIDTH - player_size:
            player_x += player_speed

        # Bullet firing with cooldown
        if keys[pygame.K_SPACE] and bullet_timer == 0:
            bullets.append([player_x + player_size//2, player_y])
            bullet_timer = bullet_cooldown
            # play_shoot_sound()  # Uncomment if sound is implemented

        if bullet_timer > 0:
            bullet_timer -= 1

        # Update bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if frame_count % spawn_delay == 0:
            enemy_x = random.randint(0, WIDTH - enemy_size)
            enemies.append([enemy_x, 0])

        # Update enemies
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                game_over = True
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)

        # Collision detection
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                bx, by = bullet
                ex, ey = enemy
                if ex < bx < ex + enemy_size and ey < by < ey + enemy_size:
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    explosions.append((ex + enemy_size//2, ey + enemy_size//2, explosion_duration))
                    score += 1
                    # play_hit_sound()  # Uncomment if sound is implemented
                    break

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(win, RED, bullet, bullet_radius)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(win, BLUE, (enemy[0], enemy[1], enemy_size, enemy_size))

        # Draw player
        draw_player(player_x, player_y)

        # Draw explosions
        draw_explosions()

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

        frame_count += 1

    else:
        # Game over screen
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        win.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

        if keys[pygame.K_r]:
            reset_game()
        if keys[pygame.K_q]:
            run = False

    pygame.display.update()

pygame.quit()
sys.exit()
