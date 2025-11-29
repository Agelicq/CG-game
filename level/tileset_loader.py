import pygame
from level.tile import TILE_SIZE  # ya vale 40

import pygame

TILE_SIZE = 40  # tamaño que usa tu mapa

def load_tileset(path):
    sheet = pygame.image.load(path).convert_alpha()
    tiles = []

    TILE_ORIGINAL = 16  # tamaño real de cada tile en la imagen

    for y in range(0, 32, TILE_ORIGINAL):       # alto total = 32
        for x in range(0, 48, TILE_ORIGINAL):   # ancho total = 48
            tile = sheet.subsurface(pygame.Rect(x, y, TILE_ORIGINAL, TILE_ORIGINAL))
            tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))  # escalar a tu tamaño real
            tiles.append(tile)

    return tiles




