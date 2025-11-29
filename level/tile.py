import pygame

TILE_SIZE = 40

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None, type="solid"):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = type  




