#!/usr/bin/env python3
"""Módulo de Elementos Tóxicos del Juego.

Este módulo contiene la clase Toxic que representa
elementos tóxicos que dañan al jugador en Astro Lost.
"""

import pygame


class Toxic(pygame.sprite.Sprite):
    """Clase que representa un elemento tóxico en el juego.
    
    Los elementos tóxicos son obstáculos estáticos que causan
    daño al jugador por contacto directo.
    
    Atributos:
        image (pygame.Surface): Imagen visual del elemento tóxico.
        rect (pygame.Rect): Rectángulo de colisión del objeto.
    """
    
    def __init__(self, x, y, image):
        """Inicializa un nuevo elemento tóxico.
        
        Args:
            x (int): Coordenada X de la posición del elemento.
            y (int): Coordenada Y de la posición del elemento.
            image (pygame.Surface): Imagen del elemento tóxico.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
