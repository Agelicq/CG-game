#!/usr/bin/env python3
"""Módulo de Estalactitas del Juego.

Este módulo contiene la clase Stalactite que representa
estalactitas que caen y pueden dañar al jugador en Astro Lost.
"""

import pygame

# Constante de gravedad para las estalactitas
GRAVITY = 0.6


class Stalactite(pygame.sprite.Sprite):
    """Clase que representa una estalactita que cae en el juego.
    
    Las estalactitas cuelgan del techo y caen cuando el jugador
    se acerca, causando daño por contacto. Se reinician automáticamente
    después de tocar el suelo.
    
    Atributos:
        start_x (int): Coordenada X inicial para reinicio.
        start_y (int): Coordenada Y inicial para reinicio.
        image (pygame.Surface): Imagen visual de la estalactita.
        rect (pygame.Rect): Rectángulo de colisión.
        falling (bool): Estado de caída de la estalactita.
        fall_speed (int): Velocidad de caída en píxeles por frame.
    """
    
    def __init__(self, x, y, image):
        """Inicializa una nueva estalactita.
        
        Args:
            x (int): Coordenada X de la posición inicial.
            y (int): Coordenada Y de la posición inicial.
            image (pygame.Surface): Imagen de la estalactita.
        """
        super().__init__()
        self.start_x = x
        self.start_y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.falling = False
        self.fall_speed = 3

    def update(self, player, tiles):
        self.falling = True

        # Si está cayendo
        if self.falling:
            self.rect.y += self.fall_speed

            # Si toca suelo / reiniciar para caer otra vez
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    self.reset()
                    break

            # Si sale de pantalla por abajo / reiniciar también
            if self.rect.top > 600:  # alto de pantalla
                self.reset()

            # colisión con el jugador
            if self.rect.colliderect(player.rect):
                player.take_damage(15)
                self.reset()
                return

            # colisión con tiles
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    self.kill()
                    return


    def reset(self):
        self.rect.topleft = (self.start_x, self.start_y)
        self.falling = False
