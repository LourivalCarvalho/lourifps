import pygame
import random

class ParticlesBrokenTarget:
    def __init__(self):
        self.particles = pygame.sprite.Group()

    def create_particles(self, x, y, image):
        for _ in range(3):
            particle = pygame.sprite.Sprite()
            particle.image = image
            particle.rect = particle.image.get_rect(center=(x+random.uniform(-150, 150), y+random.uniform(-150, 150)))
            particle.speed_x = random.uniform(-100, 100)
            particle.speed_y = random.uniform(-100, 100)
            particle.angle = random.uniform(0, 360)
            particle.rotation_speed = random.uniform(-10, 10)
            particle.lifetime = 7
            self.particles.add(particle)

    def update(self):
        for particle in self.particles:
            particle.rect.x += particle.speed_x
            particle.rect.y += particle.speed_y
            particle.angle += particle.rotation_speed
            if particle.angle >= 360:
                particle.angle -= 360
            particle.image = pygame.transform.rotate(particle.image, particle.angle)
            particle.lifetime -= 1
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        self.particles.draw(screen)
