import pygame
from level.tile import Tile, TILE_SIZE
from level.world_loader import load_map

class Level:
    def __init__(self, planet_name):
        self.tiles = pygame.sprite.Group()
        self.player_spawn = (0, 0)  # si no hay P en el mapa, aparece en (0, 0)

        self.load_level(planet_name)

    def load_level(self, planet_name):
        layout = load_map(planet_name)

        img_block = pygame.Surface((TILE_SIZE, TILE_SIZE))
        img_block.fill((120, 120, 120))  # bloque provisional

        for row_idx, row in enumerate(layout):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE

                if cell == "1" or cell == "#":  # plataforma sólida
                    tile = Tile((x, y), img_block)
                    self.tiles.add(tile)

                elif cell == "P":  # jugador aparece aquí
                    self.player_spawn = (x, y)

    def draw(self, surface):
        self.tiles.draw(surface)
