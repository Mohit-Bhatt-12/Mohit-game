import pygame
import random
import sys
import os
import time

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

# Load Images Safely
def load_image(path, size=None):
    try:
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception as e:
        print(f"[ERROR] Couldn't load image {path}: {e}")
        return pygame.Surface((50, 50))

player_img = load_image("player.png", (50, 50))
enemy_img = load_image("ghost.png", (60, 60))
background_img = load_image("background.png", (WIDTH, HEIGHT))
panel_background = load_image("panel_background.png", (WIDTH, HEIGHT))

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
                if event.key == pygame.K_1 or event.unicode == '1':
                    return 2, 1, 0.1
                elif event.key == pygame.K_2 or event.unicode == '2':
                    return 4, 2, 0.2
                elif event.key == pygame.K_3 or event.unicode == '3':
                    return 6, 4, 0.3

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
                if event.key == pygame.K_1 or event.unicode == '1':
                    return "REPLAY"
                elif event.key == pygame.K_2 or event.unicode == '2':
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
    enemy_speed, max_enemies, enemy_spawn_rate = difficulty_panel()

    score = 0
    enemies = []
    enemy_bullets = []
    player_bullets = []
    player_rect = player_img.get_rect(topleft=(100, HEIGHT // 2))

    playing = True

    while playing:
        screen.fill(WHITE)
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_shoot()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed

        for bullet in player_bullets[:]:
            bullet.x += bullet_speed
            if bullet.x > WIDTH:
                player_bullets.remove(bullet)
            pygame.draw.rect(screen, BLUE, bullet)

        if random.random() < enemy_spawn_rate and len(enemies) < max_enemies:
            enemy_rect = enemy_img.get_rect(topleft=(WIDTH, random.randint(0, HEIGHT - 60)))
            enemies.append(enemy_rect)

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

        for bullet in player_bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    player_bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        screen.blit(player_img, player_rect)

        score_text = font.render(f"Score: {score}", True, YELLOW)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
