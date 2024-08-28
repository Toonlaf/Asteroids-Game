import pygame
import random
from constants import *
from shot import Shot

class SmokeParticle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(random.uniform(-10, 10), random.uniform(-10, 10))
        self.lifetime = random.uniform(0.4, 0.8)  # Increased lifetime
        self.color = (150, 150, 150, 255)  # Lighter gray for more visibility
        self.radius = random.uniform(3, 6)  # Increased size range

    def update(self, dt):
        self.pos += self.vel * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        else:
            alpha = int(200 * (self.lifetime / 1.5))  # Start fading from a higher alpha
            self.color = (*self.color[:3], alpha)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), int(self.radius))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface((60, 48), pygame.SRCALPHA)
        
        # Draw the main body of the ship
        pygame.draw.polygon(self.original_image, (100, 100, 100), [(30, 0), (0, 48), (60, 48)])
        
        # Draw the cockpit
        pygame.draw.ellipse(self.original_image, (0, 200, 255), (20, 10, 20, 25))
        pygame.draw.ellipse(self.original_image, (150, 230, 255), (23, 13, 14, 19))
        
        # Draw the wings
        pygame.draw.polygon(self.original_image, (180, 0, 0), [(0, 48), (20, 20), (25, 48)])
        pygame.draw.polygon(self.original_image, (180, 0, 0), [(60, 48), (40, 20), (35, 48)])
        
        # Add engine exhausts
        pygame.draw.rect(self.original_image, (255, 150, 0), (10, 44, 10, 4))
        pygame.draw.rect(self.original_image, (255, 150, 0), (40, 44, 10, 4))
        
        # Add some details
        pygame.draw.line(self.original_image, (255, 255, 0), (0, 48), (60, 48), 2)
        pygame.draw.line(self.original_image, (255, 255, 0), (15, 30), (45, 30), 2)
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.smoke_particles = pygame.sprite.Group()
        self.smoke_timer = 0
        self.smoke_interval = 0.02  # Emit smoke more frequently

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Rotate left
            self.rotation += PLAYER_TURN_SPEED * dt
        if keys[pygame.K_d]:  # Rotate right
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_w]:  # Move forward
            acceleration = pygame.Vector2(0, -PLAYER_SPEED).rotate(-self.rotation)
            self.velocity += acceleration * dt

        self.velocity *= 0.98  # Add some drag

        self.position += self.velocity * dt
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)

        # Emit smoke particles
        self.smoke_timer += dt
        if self.smoke_timer >= self.smoke_interval:
            self.smoke_timer = 0
            self.emit_smoke()

        # Update smoke particles
        self.smoke_particles.update(dt)

    def shoot(self):
        front_offset = pygame.Vector2(0, -self.rect.height / 2).rotate(-self.rotation)
        shot_pos = self.position + front_offset
        return Shot(shot_pos.x, shot_pos.y, self.rotation)

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)

    def reset(self):
        self.position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.rect.center = self.position

    def emit_smoke(self):
        # Calculate positions for smoke emission (from the engine exhausts)
        left_exhaust = self.position + pygame.Vector2(-20, 22).rotate(-self.rotation)
        right_exhaust = self.position + pygame.Vector2(20, 22).rotate(-self.rotation)
        
        # Emit multiple particles per frame
        for _ in range(3):  # Increased from 1 to 3 particles per emission
            self.smoke_particles.add(SmokeParticle(left_exhaust))
            self.smoke_particles.add(SmokeParticle(right_exhaust))

    def draw(self, surface):
        # Draw smoke particles
        for particle in self.smoke_particles:
            particle.draw(surface)
        
        # Draw the player
        surface.blit(self.image, self.rect)