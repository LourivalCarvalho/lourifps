import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-0.3, 0.3)
        self.gravity = 0.001  # força da gravidade
        self.radius = random.randint(3, 7)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.lifetime = random.uniform(870, 2000)  # em milissegundos
        self.creation_time = pygame.time.get_ticks()
        self.opacity = 255  # inicialmente 100% de opacidade

    def update(self):
        self.x += self.vx
        self.vy += self.gravity  # aplicar força da gravidade
        self.y += self.vy
        current_time = pygame.time.get_ticks()
        self.opacity = int(255 * (1 - (current_time - self.creation_time) / self.lifetime))

    def is_alive(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.creation_time < self.lifetime

    def draw(self, screen):
        surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (self.color[0], self.color[1], self.color[2], self.opacity), (self.radius, self.radius), self.radius)
        screen.blit(surface, (int(self.x - self.radius), int(self.y - self.radius)))

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