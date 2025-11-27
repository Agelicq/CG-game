import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(self.image, (75, 65))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.collected = False
