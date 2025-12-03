
"""Módulo de Tile del Juego.

Este módulo contiene la clase Tile que representa los bloques
individuales que forman los niveles en Astro Lost.
"""

import pygame

# Constante global para el tamaño de cada tile
TILE_SIZE = 40


class Tile(pygame.sprite.Sprite):
    """Clase que representa un tile individual del nivel.
    
    Un tile es un bloque básico que forma parte del mapa del nivel.
    Puede ser sólido, hielo, lava, escalable, etc.
    
    Atributos:
        image (pygame.Surface): Imagen visual del tile.
        rect (pygame.Rect): Rectángulo de colisión del tile.
        type (str): Tipo de tile que determina su comportamiento.
    """
    
    def __init__(self, x, y, image=None, type="solid"):
        """Inicializa un nuevo tile.
        
        Args:
            x (int): Coordenada X de la posición del tile.
            y (int): Coordenada Y de la posición del tile.
            image (pygame.Surface, optional): Imagen del tile. Por defecto None.
            type (str): Tipo de tile ('solid', 'ice', 'lava', etc.). 
            Por defecto 'solid'.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = type  




