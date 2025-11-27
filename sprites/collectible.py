import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image, type="fragment"):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.type = type   # "fragment" o "heal"
