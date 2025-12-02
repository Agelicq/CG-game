import pygame
import time

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, length, interval=2):
        super().__init__()
        self.x = x
        self.y = y
        self.length = length
        self.interval = interval  # seconds ON / OFF
        self.active = False
        self.timer = 0

    def update(self, dt, player):
        self.timer += dt
        if self.timer >= self.interval:
            self.timer = 0
            self.active = not self.active  # toggle

        if self.active:
            laser_rect = pygame.Rect(self.x, self.y, 6, self.length)
            if laser_rect.colliderect(player.rect):
                player.take_damage(10)   # daño por contacto

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 3, self.length))
