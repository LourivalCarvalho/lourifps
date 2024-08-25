import pygame
import random
import os

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-.1, .1)
        self.vy = random.uniform(-.8, -5.5)
        self.lifetime = random.uniform(750, 1250) 
        self.creation_time = pygame.time.get_ticks()
        self.opacity = 255

        # Load sprites
        sprite_folder = os.path.join(os.path.dirname(__file__), 'assets/')
        self.sprites = []
        for filename in ['smoke1.png', 'smoke2.png', 'smoke3.png']:
            width = random.randint(48, 200)
            height = width
            sprite = pygame.transform.scale(pygame.image.load(os.path.join(sprite_folder, filename)).convert_alpha(), (width, height))
            self.sprites.append(sprite)
        self.sprite = random.choice(self.sprites)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        current_time = pygame.time.get_ticks()
        self.opacity = int(255 * (1 - (current_time - self.creation_time) / self.lifetime))

    def is_alive(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.creation_time < self.lifetime

    def draw(self, screen):
        image = self.sprite
        image.set_alpha(self.opacity)
        screen.blit(image, (int(self.x - image.get_width() / 2), int(self.y - image.get_height() / 2)))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particles(self, x, y, num_particles):
        for _ in range(num_particles):
            self.particles.append(Particle(x, y))

    def update(self):
        for particle in self.particles:
            particle.update()
            if not particle.is_alive() or particle.x < 0 or particle.x > 1280 or particle.y < 0 or particle.y > 720:
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)