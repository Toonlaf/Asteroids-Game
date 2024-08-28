import pygame
import sys
import random
import math
from constants import *
from player import Player
from asteroid import Asteroid
from shot import Shot

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
all_sprites.add(player)

score = 0
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 84)

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "Easy": {"asteroid_speed": 50, "spawn_rate": 3, "max_asteroids": 5, "color": (0, 255, 0)},
    "Medium": {"asteroid_speed": 75, "spawn_rate": 2, "max_asteroids": 7, "color": (255, 255, 0)},
    "Hard": {"asteroid_speed": 100, "spawn_rate": 1, "max_asteroids": 10, "color": (255, 0, 0)}
}

current_difficulty = "Medium"

def create_star_field(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        speed = random.uniform(10, 50)
        stars.append([x, y, speed])
    return stars

def update_star_field(stars, dt):
    for star in stars:
        star[1] += star[2] * dt
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)

def draw_star_field(surface, stars):
    for star in stars:
        pygame.draw.circle(surface, (255, 255, 255), (int(star[0]), int(star[1])), 1)

def create_background_asteroids(num_asteroids):
    bg_asteroids = []
    for _ in range(num_asteroids):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        speed = random.randint(20, 50)
        angle = random.uniform(0, 360)
        velocity = pygame.Vector2(speed, 0).rotate(angle)
        size = random.randint(10, 30)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        bg_asteroids.append({"pos": pygame.Vector2(x, y), "vel": velocity, "size": size, "color": color})
    return bg_asteroids

def update_background_asteroids(bg_asteroids, dt):
    for asteroid in bg_asteroids:
        asteroid["pos"] += asteroid["vel"] * dt
        if asteroid["pos"].x < -50:
            asteroid["pos"].x = SCREEN_WIDTH + 50
        elif asteroid["pos"].x > SCREEN_WIDTH + 50:
            asteroid["pos"].x = -50
        if asteroid["pos"].y < -50:
            asteroid["pos"].y = SCREEN_HEIGHT + 50
        elif asteroid["pos"].y > SCREEN_HEIGHT + 50:
            asteroid["pos"].y = -50

def draw_background_asteroids(surface, bg_asteroids):
    for asteroid in bg_asteroids:
        pygame.draw.circle(surface, asteroid["color"], (int(asteroid["pos"].x), int(asteroid["pos"].y)), asteroid["size"], 2)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, font, color, x, y, width, height, active):
    button_color = (100, 100, 100) if active else (50, 50, 50)
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

def spawn_asteroid(speed):
    asteroid = Asteroid.spawn_asteroid(speed)
    all_sprites.add(asteroid)
    asteroids.add(asteroid)
    return asteroid

def game_over_screen():
    screen.fill((0, 0, 0))
    draw_text("GAME OVER", title_font, (255, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(f"Final Score: {score}", font, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press SPACE to play again", font, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False


def start_screen():
    global current_difficulty
    difficulties = ["Easy", "Medium", "Hard"]
    button_width, button_height = 150, 60
    button_y = SCREEN_HEIGHT // 2 + 50
    buttons = []

    stars = create_star_field(100)
    bg_asteroids = create_background_asteroids(10)

    title_size = 84 + int(10 * math.sin(pygame.time.get_ticks() * 0.005))
    title_font = pygame.font.Font(None, title_size)
    title_color = [255, 255, 255]
    color_change_speed = 50

    waiting = True
    while waiting:
        dt = clock.tick(60) / 1000
        screen.fill((0, 0, 0))

        # Update and draw star field
        update_star_field(stars, dt)
        draw_star_field(screen, stars)

        # Update and draw background asteroids
        update_background_asteroids(bg_asteroids, dt)
        draw_background_asteroids(screen, bg_asteroids)

        # Animate title color
        title_color[0] = (title_color[0] + color_change_speed * dt) % 256
        title_color[1] = (title_color[1] + color_change_speed * dt * 0.5) % 256
        title_color[2] = (title_color[2] + color_change_speed * dt * 0.25) % 256

        # Draw title with shadow effect
        shadow_color = (20, 20, 20)  # Dark gray for shadow
        shadow_offset = 4  # Pixels to offset the shadow

        for i in range(3):  # Create multiple layers for a softer shadow
            alpha = 100 - i * 30  # Fade out for each layer
            shadow_font = pygame.font.Font(None, 84 + i * 2)
            shadow_surface = shadow_font.render("ASTEROIDS", True, (*shadow_color, alpha))
            shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + shadow_offset, SCREEN_HEIGHT // 4 + shadow_offset))
            screen.blit(shadow_surface, shadow_rect)

        # Draw main title text
        main_surface = title_font.render("ASTEROIDS", True, title_color)
        main_rect = main_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(main_surface, main_rect)

        draw_text("Select Difficulty:", font, (200, 200, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)

        mouse_pos = pygame.mouse.get_pos()

        for i, diff in enumerate(difficulties):
            button_x = SCREEN_WIDTH // 2 + (i - 1) * (button_width + 30) - button_width // 2
            active = diff == current_difficulty
            color = DIFFICULTY_SETTINGS[diff]["color"]
            button = draw_button(diff, font, color, button_x, button_y, button_width, button_height, active)
            buttons.append((button, diff))

        draw_text("Press SPACE to start", font, (200, 200, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 + 50)
        draw_text("W A D to move, SPACE to shoot", font, (150, 150, 150), SCREEN_WIDTH // 2, SCREEN_HEIGHT * 7 // 8)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, diff in buttons:
                    if button.collidepoint(mouse_pos):
                        current_difficulty = diff
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_loop():
    global score
    score = 0
    all_sprites.empty()
    asteroids.empty()
    shots.empty()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites.add(player)

    settings = DIFFICULTY_SETTINGS[current_difficulty]
    asteroid_timer = 0

    shot_particles = pygame.sprite.Group()

    # Spawn initial asteroids
    for _ in range(settings["max_asteroids"] // 2):
        new_asteroid = Asteroid.spawn_asteroid(settings["asteroid_speed"], asteroids)
        if new_asteroid:
            all_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)

    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shot = player.shoot()
                    all_sprites.add(shot)
                    shots.add(shot)
                    shot_particles.add(shot.create_particles())

        # Update
        all_sprites.update(dt)
        player.update(dt)
        shot_particles.update(dt)

        # Remove asteroids that are far off-screen
        for asteroid in list(asteroids):
            if asteroid.is_off_screen():
                asteroid.kill()

        # Spawn new asteroids
        asteroid_timer += dt
        if asteroid_timer >= settings["spawn_rate"] and len(asteroids) < settings["max_asteroids"]:
            new_asteroid = Asteroid.spawn_asteroid(settings["asteroid_speed"], asteroids)
            if new_asteroid:
                all_sprites.add(new_asteroid)
                asteroids.add(new_asteroid)
                asteroid_timer = 0

        # Check for collisions
        for asteroid in asteroids:
            if pygame.sprite.collide_mask(player, asteroid):
                return True  # Game over

        for shot in shots:
            hit_asteroids = pygame.sprite.spritecollide(shot, asteroids, False, pygame.sprite.collide_mask)
            for asteroid in hit_asteroids:
                asteroid.kill()
                shot.kill()
                score += 10
                # Spawn a new asteroid to replace the destroyed one
                new_asteroid = Asteroid.spawn_asteroid(settings["asteroid_speed"], asteroids)
                if new_asteroid:
                    all_sprites.add(new_asteroid)
                    asteroids.add(new_asteroid)

        # Check for asteroid-asteroid collisions
        for i, asteroid1 in enumerate(asteroids):
            for asteroid2 in list(asteroids)[i+1:]:
                if pygame.sprite.collide_mask(asteroid1, asteroid2):
                    asteroid1.collide_with_asteroid(asteroid2)

        # Ensure minimum number of asteroids
        while len(asteroids) < settings["max_asteroids"]:
            new_asteroid = Asteroid.spawn_asteroid(settings["asteroid_speed"], asteroids)
            if new_asteroid:
                all_sprites.add(new_asteroid)
                asteroids.add(new_asteroid)
            else:
                break  # Stop trying to spawn if we can't find a valid position

        # Draw everything
        screen.fill((0, 0, 0))
        player.draw(screen)  # This will draw both smoke and the player
        all_sprites.draw(screen)
        shot_particles.draw(screen)

        # Draw score and difficulty
        draw_text(f"Score: {score}", font, (255, 255, 255), 70, 20)
        draw_text(f"Difficulty: {current_difficulty}", font, settings["color"], SCREEN_WIDTH - 100, 20)

        pygame.display.flip()

    return False
def main():
    while True:
        start_screen()
        game_over = game_loop()
        if game_over:
            game_over_screen()
        else:
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()