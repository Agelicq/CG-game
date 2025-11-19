import pygame

TILE_SIZE = 40

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, solid=True):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.solid = solid  # algunos tiles en el futuro no serán sólidos
