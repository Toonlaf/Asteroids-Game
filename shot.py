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
        print(f"Shot created with angle: {angle}")
        print(f"Shot velocity: {self.velocity}")

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