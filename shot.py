import pygame
import random
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 255, 0))  # Yellow color for the shot
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 500
        self.angle = angle  # Store the angle
        # Calculate velocity based on angle
        self.velocity = pygame.math.Vector2(0, -self.speed).rotate(-angle)
        self.position = pygame.math.Vector2(x, y)
        self.lifetime = 1.5  # Shot disappears after 1.5 seconds
        self.smoke_timer = 0
        self.smoke_interval = 0.05  # Create smoke every 0.05 seconds

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

        # Remove if out of screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
           self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # Create smoke
        self.smoke_timer += dt
        if self.smoke_timer >= self.smoke_interval:
            self.smoke_timer = 0
            return [SmokeParticle(self.rect.center)]
        return []

    def create_particles(self):
        particles = []
        for _ in range(5):  # Create 5 particles per shot
            particle = ShotParticle(self.rect.center, self.angle)
            particles.append(particle)
        return particles

class ShotParticle(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 165, 0))  # Orange color for particles
        self.rect = self.image.get_rect()
        self.rect.center = pos
        speed = random.uniform(150, 250)
        angle_offset = random.uniform(-30, 30)
        self.velocity = pygame.math.Vector2(0, -speed).rotate(-(angle + angle_offset))
        self.position = pygame.math.Vector2(pos)
        self.lifetime = random.uniform(0.2, 0.5)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

class SmokeParticle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        size = random.randint(2, 5)
        self.image = pygame.Surface((size, size))
        self.image.fill((200, 200, 200))  # Gray color for smoke
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.velocity = pygame.math.Vector2(random.uniform(-20, 20), random.uniform(50, 100))
        self.position = pygame.math.Vector2(pos)
        self.lifetime = random.uniform(0.5, 1.5)
        self.alpha = 255

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        self.lifetime -= dt
        self.alpha = max(0, int(255 * (self.lifetime / 1.5)))
        self.image.set_alpha(self.alpha)
        if self.lifetime <= 0:
            self.kill()