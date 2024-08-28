import pygame
import random
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed):
        super().__init__()
        self.size = size
        self.speed = speed
        self.angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(speed, 0).rotate(self.angle)
        
        self.original_image = self.create_asteroid_shape()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.rotation = 0
        self.rotation_speed = random.uniform(-50, 50)  # Degrees per second
        
        self.mask = pygame.mask.from_surface(self.image)

    def create_asteroid_shape(self):
        num_points = random.randint(6, 10)
        points = []
        for i in range(num_points):
            angle = i * (360 / num_points) + random.uniform(-20, 20)
            radius = self.size * random.uniform(0.7, 1.0)
            x = self.size + radius * math.cos(math.radians(angle))
            y = self.size + radius * math.sin(math.radians(angle))
            points.append((x, y))

        # Generate a random pale color
        base_color = random.choice([
            (210, 180, 140),  # Tan
            (192, 192, 192),  # Silver
            (169, 169, 169),  # Dark Gray
            (200, 200, 169),  # Pale Gold
            (180, 180, 200),  # Pale Blue-Gray
            (200, 180, 180),  # Pale Pink-Gray
        ])
        
        # Add some slight randomness to the color
        color = tuple(max(0, min(255, c + random.randint(-20, 20))) for c in base_color)
        
        image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.polygon(image, color, points, 0)  # Fill with pale color
        
        # Create a slightly darker outline
        outline_color = tuple(max(0, c - 30) for c in color)
        pygame.draw.polygon(image, outline_color, points, 2)  # Outline
        
        return image

    def update(self, dt):
        self.position += self.velocity * dt
        
        # Wrap around the screen with a buffer zone
        buffer = self.size * 2
        if self.position.x < -buffer:
            self.position.x = SCREEN_WIDTH + buffer
        elif self.position.x > SCREEN_WIDTH + buffer:
            self.position.x = -buffer
        if self.position.y < -buffer:
            self.position.y = SCREEN_HEIGHT + buffer
        elif self.position.y > SCREEN_HEIGHT + buffer:
            self.position.y = -buffer
        
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def collide_with_asteroid(self, other_asteroid):
        # Simple elastic collision
        normal = self.position - other_asteroid.position
        normal = normal.normalize()
        relative_velocity = self.velocity - other_asteroid.velocity
        
        speed_change = 2 * relative_velocity.dot(normal) / (self.size + other_asteroid.size)
        self.velocity -= speed_change * other_asteroid.size * normal
        other_asteroid.velocity += speed_change * self.size * normal

    @staticmethod
    def spawn_asteroid(speed, existing_asteroids):
        size = random.randint(20, 50)
        buffer = size * 2  # Buffer zone for spawning
        
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            # Randomly choose a side to spawn from
            side = random.choice(['top', 'bottom', 'left', 'right'])
            
            if side == 'top':
                x = random.randint(-buffer, SCREEN_WIDTH + buffer)
                y = -buffer
            elif side == 'bottom':
                x = random.randint(-buffer, SCREEN_WIDTH + buffer)
                y = SCREEN_HEIGHT + buffer
            elif side == 'left':
                x = -buffer
                y = random.randint(-buffer, SCREEN_HEIGHT + buffer)
            else:  # right
                x = SCREEN_WIDTH + buffer
                y = random.randint(-buffer, SCREEN_HEIGHT + buffer)
            
            new_asteroid = Asteroid(x, y, size, speed)
            
            # Check if the new asteroid overlaps with any existing asteroids
            if not any(pygame.sprite.collide_mask(new_asteroid, existing) for existing in existing_asteroids):
                return new_asteroid
            
            attempts += 1
        
        # If we couldn't find a non-overlapping position, return None
        return None

    def is_off_screen(self):
        buffer = self.size * 2
        return (self.position.x < -buffer or 
                self.position.x > SCREEN_WIDTH + buffer or 
                self.position.y < -buffer or 
                self.position.y > SCREEN_HEIGHT + buffer)