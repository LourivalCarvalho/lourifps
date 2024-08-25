import pygame
import random
import config

screen_width = config.SCREEN_WIDTH

class ClayPigeon:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load('assets/target_clay_pigeon.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed_x = 21
        self.speed_y = -14
        self.direction = 1  # 1 for left to right, -1 for right to left
        self.launched = False

    def launch(self, screen_width, screen_height):
        self.direction *= -1 # Reverses the launch direction of the clay pigeon: right or left
        self.image = pygame.transform.flip(self.image, True, False) # Flips the image horizontally
        if self.direction == 1:
            self.rect.x = 0
            self.rect.y = screen_height - self.rect.height
        else:
            self.rect.x = screen_width - self.rect.width
            self.rect.y = screen_height - self.rect.height
        self.launched = True

    def update(self):
        if self.launched:
            self.rect.x += self.speed_x * self.direction
            self.rect.y += self.speed_y
            if self.rect.y < 0 or self.rect.x < 0 or self.rect.x > screen_width:
                self.launched = False

    def draw(self, screen):
        if self.launched:
            screen.blit(self.image, self.rect)

import pygame
import random

class Balloon:
    def __init__(self, screen_width, screen_height):
        self.original_image = pygame.image.load('assets/target_balloon.png').convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.speed_y = -14
        self.launched = False

    def colorize(self):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                r0, g0, b0, a0 = self.original_image.get_at((x, y))
                r1, g1, b1 = self.colorize_pixel(r0, g0, b0, r, g, b)
                self.image.set_at((x, y), (r1, g1, b1, a0))

    def colorize_pixel(self, r0, g0, b0, r, g, b):
        r1 = max(0, min(int(r0 * r / 255), 255))
        g1 = max(0, min(int(g0 * g / 255), 255))
        b1 = max(0, min(int(b0 * b / 255), 255))
        return r1, g1, b1

    def launch(self, screen_width, screen_height):
        self.colorize()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = screen_height - self.rect.height
        self.launched = True

    def update(self):
        if self.launched:
            self.rect.y += self.speed_y
            if self.rect.y < 0:
                self.launched = False

    def draw(self, screen):
        if self.launched:
            screen.blit(self.image, self.rect)


# For future update to transform the target 1 into a class and add some animation.
# Not used yet
'''
class Target:
    def __init__(self, image_path, screen_width, screen_height):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, max(0, screen_height - self.rect.height))
        self.scale_factor = 1.0
        self.destroyed = False

    def shrink(self):
        self.scale_factor -= 0.01
        if self.scale_factor < 0.05:
            self.destroyed = True
        self.rect.width = int(self.image.get_width() * self.scale_factor)
        self.rect.height = int(self.image.get_height() * self.scale_factor)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
'''