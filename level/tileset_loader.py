#!/usr/bin/env python3
"""Cargador de Tilesets del Juego.

Este módulo proporciona funciones para cargar y procesar
hojas de sprites (tilesets) para los niveles de Astro Lost.
"""

import pygame

from level.tile import TILE_SIZE

# Tamaño original de cada tile en la imagen del tileset
TILE_ORIGINAL = 16

def load_tileset(path):
    """Carga un tileset desde una imagen y lo divide en tiles individuales.
    
    Toma una hoja de sprites y la divide en tiles individuales,
    escalándolos al tamaño requerido por el juego.
    
    Args:
        path (str): Ruta al archivo de imagen del tileset.
        
    Returns:
        list: Lista de superficies pygame con cada tile individual.
        
    Raises:
        pygame.error: Si no se puede cargar la imagen del tileset.
    """
    sheet = pygame.image.load(path).convert_alpha()
    tiles = []

    # Recorrer la hoja de sprites y extraer cada tile
    for y in range(0, 32, TILE_ORIGINAL):       # Alto total = 32 píxeles
        for x in range(0, 48, TILE_ORIGINAL):   # Ancho total = 48 píxeles
            # Extraer el tile individual de la hoja
            tile = sheet.subsurface(pygame.Rect(x, y, TILE_ORIGINAL, TILE_ORIGINAL))
            # Escalar al tamaño requerido por el juego
            tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
            tiles.append(tile)

    return tiles




