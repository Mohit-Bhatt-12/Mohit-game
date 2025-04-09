import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game By Mohit Bhatt")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Game Variables
clock = pygame.time.Clock()
FPS = 60
player_speed = 5
bullet_speed = 10
enemy_bullet_speed = 5
font = pygame.font.SysFont(None, 40)

# Load Images
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("ghost.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 60))

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

panel_background = pygame.image.load("panel_background.png")
panel_background = pygame.transform.scale(panel_background, (WIDTH, HEIGHT))

def difficulty_panel():
    while True:
        screen.fill(WHITE)
        screen.blit(panel_background, (0, 0))

        title_text = font.render("Choose Difficulty", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - 120, 50))

        easy_text = font.render("1. Easy", True, YELLOW)
        screen.blit(easy_text, (WIDTH // 2 - 60, 150))

        medium_text = font.render("2. Medium", True, YELLOW)
        screen.blit(medium_text, (WIDTH // 2 - 60, 200))

        hard_text = font.render("3. Hard", True, YELLOW)
        screen.blit(hard_text, (WIDTH // 2 - 60, 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 2, 1, 0.1   # Easy -> Slowest Enemy Speed
                elif event.key == pygame.K_2:
                    return 4, 2, 0.2   # Medium -> Moderate Enemy Speed
                elif event.key == pygame.K_3:
                    return 6, 4, 0.3   # Hard -> Fastest Enemy Speed

# Panel After Game Over
def end_panel():
    while True:
        screen.fill(WHITE)
        screen.blit(panel_background, (0, 0))

        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 80, 100))

        replay_text = font.render("1. Replay", True, YELLOW)
        screen.blit(replay_text, (WIDTH // 2 - 60, 200))

        exit_text = font.render("2. Exit", True, YELLOW)
        screen.blit(exit_text, (WIDTH // 2 - 60, 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "REPLAY"
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

# Shooting functions
def player_shoot():
    bullet = pygame.Rect(player_rect.centerx + 20, player_rect.centery, 5, 5)
    player_bullets.append(bullet)

def enemy_shoot(enemy):
    if random.random() < 0.01:
        bullet = pygame.Rect(enemy.centerx - 10, enemy.centery, 5, 5)
        enemy_bullets.append(bullet)

# Main Game Loop
while True:
    # Get chosen difficulty
    enemy_speed, max_enemies, enemy_spawn_rate = difficulty_panel()
    
    # Reset Game Variables
    score = 0
    enemies = []
    enemy_bullets = []
    player_bullets = []
    player_rect = player_img.get_rect(topleft=(100, HEIGHT // 2))

    playing = True

    while playing:  # Game Loop
        screen.fill(WHITE)
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_shoot()

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed

        # Move and Draw Player Bullets
        for bullet in player_bullets[:]:
            bullet.x += bullet_speed
            if bullet.x > WIDTH:
                player_bullets.remove(bullet)
            pygame.draw.rect(screen, BLUE, bullet)

        # Spawn Enemies
        if random.random() < enemy_spawn_rate and len(enemies) < max_enemies:
            enemy_rect = enemy_img.get_rect(topleft=(WIDTH, random.randint(0, HEIGHT - 60)))
            enemies.append(enemy_rect)

        # Move and Draw Enemies
        for enemy in enemies[:]:
            enemy.x -= enemy_speed
            if enemy.x < 0:
                enemies.remove(enemy)
            else:
                screen.blit(enemy_img, enemy)
                enemy_shoot(enemy)

            if player_rect.colliderect(enemy):
                if end_panel() == "REPLAY":
                    playing = False
                    break
                else:
                    pygame.quit()
                    sys.exit()

        # Move and Draw Enemy Bullets
        for bullet in enemy_bullets[:]:
            bullet.x -= enemy_bullet_speed
            if bullet.x < 0:
                enemy_bullets.remove(bullet)
            if bullet.colliderect(player_rect):
                if end_panel() == "REPLAY":
                    playing = False
                    break
                else:
                    pygame.quit()
                    sys.exit()
            pygame.draw.rect(screen, RED, bullet)

        # Bullet Collision with Enemies
        for bullet in player_bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    player_bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # Draw Player
        screen.blit(player_img, player_rect)

        # Display Score
        score_text = font.render(f"Score: {score}", True, YELLOW)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
