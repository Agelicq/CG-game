
"""Módulo de Coleccionables del Juego.

Este módulo contiene la clase Collectible que representa
objetos que el jugador puede recoger en Astro Lost.
"""

import pygame


class Collectible(pygame.sprite.Sprite):
    """Clase que representa un objeto coleccionable en el juego.
    
    Los coleccionables son objetos que el jugador puede recoger
    para obtener beneficios como fragmentos de energía o curación.
    
    Atributos:
        image (pygame.Surface): Imagen visual del coleccionable.
        rect (pygame.Rect): Rectángulo de colisión del objeto.
        type (str): Tipo de coleccionable ('fragment' o 'heal').
    """
    
    def __init__(self, x, y, image, type="fragment"):
        """Inicializa un nuevo coleccionable.
        
        Args:
            x (int): Coordenada X de la posición del objeto.
            y (int): Coordenada Y de la posición del objeto.
            image (pygame.Surface): Imagen del coleccionable.
            type (str): Tipo de coleccionable. Opciones:
                       'fragment' - Fragmento de energía
                       'heal' - Objeto de curación
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.type = type   # "fragment" o "heal"
