import pygame
from level.tile import Tile, TILE_SIZE
from level.world_loader import load_map

class Level:
    def __init__(self, planet_name):
        self.tiles = pygame.sprite.Group()
        self.load_level(planet_name)

    def load_level(self, planet_name):
        layout = load_map(planet_name)

        # Por ahora un bloque gris temporal
        img_block = pygame.Surface((TILE_SIZE, TILE_SIZE))
        img_block.fill((120, 120, 120))

        for row_idx, row in enumerate(layout):
            for col_idx, cell in enumerate(row):
                if cell == "1":
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    tile = Tile((x, y), img_block)
                    self.tiles.add(tile)

    def draw(self, surface):
        self.tiles.draw(surface)
