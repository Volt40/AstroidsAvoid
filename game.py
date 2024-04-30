import pygame
import sys
import random
import math

from star import Star
from asteroid import Asteroid
from bomb import Bomb
from popup import create_popup

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Asteroids")
stage = 1

# Set up the player's ship
player_image = pygame.image.load("player_nf.png")
player_image_moving = pygame.image.load("player.png")
player_width = 50
player_height = 50
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player_image_moving = pygame.transform.scale(player_image_moving, (player_width, player_height))
player_rect = player_image.get_rect()
player_rect.center = (screen_width // 2, screen_height // 2)
player_vx = 0
player_vy = 0
player_acceleration = 0
player_direction = 0
moving = False

# Set up the asteroids
asteroids = []
num_asteroids = 5
for _ in range(num_asteroids):
    nA = Asteroid(
        random.randrange(0, screen_width),
        random.randrange(0, screen_height),
        random.randrange(35, 100),
        random.randrange(2, 5),
        random.randrange(0, 360))
    asteroids.append(nA)

# Set up the bombs
bombs = []
num_bombs = 3
for _ in range(num_bombs):
    nB = Bomb(
        random.randrange(0, screen_width),
        random.randrange(0, screen_height),
        random.randrange(35, 100),
        random.randrange(5, 10),
        random.randrange(0, 360))
    bombs.append(nB)

# Set up the star
star = Star(
    random.randrange(0, screen_width),
    random.randrange(0, screen_height),
    random.randrange(40),
    random.randrange(50),
    random.randrange(0, 360))

# Set up the timer font
timer_amount = 10
font = pygame.font.Font(None, 36)
timer = timer_amount
timer_text = font.render("Time: " + str(timer), True, (255, 255, 255))
timer_rect = timer_text.get_rect(topright=(screen_width - 30, 10))
stage_text = font.render("Stage #" + str(stage), True, (255, 255, 255))
stage_rect = stage_text.get_rect(topright=(screen_width - 30, 40))
hint_text = font.render("Avoid the flying objects!", True, (255, 255, 255))
hint_rect = hint_text.get_rect(topleft=(10, 20))

# Set up the enemies
enemies = []
num_enemies = 3
for _ in range(num_enemies):
    enemy_image = pygame.image.load("bomb.png")  # Add your enemy image file
    enemy_rect = enemy_image.get_rect()
    enemy_rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
    enemies.append(enemy_rect)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player's movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_direction += 10
    if keys[pygame.K_RIGHT]:
        player_direction -= 10
    if keys[pygame.K_UP]:
        player_acceleration = -1
        moving = True
    elif keys[pygame.K_DOWN]:
        player_acceleration = 1
        moving = True
    else:
        moving = False
    if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        player_acceleration = 0

    player_image_rotated = pygame.transform.rotate(player_image, player_direction)
    if moving:
        player_image_rotated = pygame.transform.rotate(player_image_moving, player_direction)
    player_rect = player_image_rotated.get_rect(center=player_rect.center)
    angle_radians = math.radians(180 - (player_direction + 90))
    player_vx += player_acceleration * math.cos(angle_radians)
    player_vy += player_acceleration * math.sin(angle_radians)
    if player_vx > 20:
        player_vx = 20
    if player_vx < -20:
        player_vx = -20
    if player_vy > 20:
        player_vy = 20
    if player_vy < -20:
        player_vy = -20
    player_rect.x += player_vx
    player_rect.y += player_vy


    # Wrap around the screen
    if player_rect.left > screen_width:
        player_rect.right = 0
    elif player_rect.right < 0:
        player_rect.left = screen_width
    if player_rect.top > screen_height:
        player_rect.bottom = 0
    elif player_rect.bottom < 0:
        player_rect.top = screen_height

    for asteroid in asteroids:
        if player_rect.colliderect(asteroid.rect):
            running = False

    if stage >= 2:
        for bomb in bombs:
            if player_rect.colliderect(bomb.rect):
                running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player's ship
    screen.blit(player_image_rotated, player_rect)

    # Draw the asteroids
    for asteroid in asteroids:
        asteroid.move()
        asteroid.render(screen)

    if stage >= 2:
        for bomb in bombs:
            bomb.move()
            bomb.render(screen)

    if stage >= 3:
        star.move()
        star.render(screen)

        # Update and draw the timer
    timer -= 1 / 30  # Decrease timer by 1/30 (30 frames per second)
    if timer < 0:
        timer = timer_amount
        stage += 1
        stage_text = font.render("Stage #" + str(stage), True, (255, 255, 255))
    timer_text = font.render("Time: " + "{:.1f}".format(timer), True, (255, 255, 255))
    screen.blit(timer_text, timer_rect)
    screen.blit(stage_text, stage_rect)
    screen.blit(hint_text, hint_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

create_popup(screen, "Gave Over!")
pygame.event.wait()

# Quit Pygame
pygame.quit()
sys.exit()
