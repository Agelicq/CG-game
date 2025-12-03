#!/usr/bin/env python3
"""Módulo de Proyectiles del Juego.

Este módulo contiene la clase Projectile que representa
los proyectiles disparados por el jugador en Astro Lost.
"""

import pygame

# Constantes de configuración del proyectil
PROJECTILE_SPEED = 12
PROJECTILE_SIZE = (20, 6)   # Tamaño ajustable según arte


class Projectile(pygame.sprite.Sprite):
    """Clase que representa un proyectil disparado por el jugador.
    
    Los proyectiles se mueven en línea recta y se destruyen
    al colisionar con tiles o al salir de la pantalla.
    
    Atributos:
        image (pygame.Surface): Imagen visual del proyectil.
        rect (pygame.Rect): Rectángulo de colisión.
        direction (int): Dirección de movimiento (1 derecha, -1 izquierda).
        speed (int): Velocidad de movimiento en píxeles por frame.
        alive (bool): Estado del proyectil (vivo/destruido).
    """
    
    def __init__(self, x, y, direction):
        """Inicializa un nuevo proyectil.
        
        Args:
            x (int): Coordenada X inicial del proyectil.
            y (int): Coordenada Y inicial del proyectil.
            direction (int): Dirección de movimiento.
                           1 para derecha, -1 para izquierda.
        """
        super().__init__()
        
        # Crear imagen visual del proyectil
        self.image = pygame.Surface(PROJECTILE_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, *PROJECTILE_SIZE))
        
        # Posicionar según dirección
        if direction > 0:
            self.rect = self.image.get_rect(midleft=(x, y))
        else:
            self.rect = self.image.get_rect(midright=(x, y))

        # Configuración de movimiento
        self.direction = direction
        self.speed = PROJECTILE_SPEED
        self.alive = True

    def update(self, tiles):
        """Actualiza la posición del proyectil y verifica colisiones.
        
        Mueve el proyectil en su dirección y lo destruye si colisiona
        con tiles o sale de los límites de la pantalla.
        
        Args:
            tiles (pygame.sprite.Group): Grupo de tiles para verificar colisiones.
        """
        # Mover proyectil
        self.rect.x += self.direction * self.speed

        # Eliminar proyectil si toca un tile
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.kill()
                return

        # Eliminar si sale de pantalla
        if self.rect.right < 0 or self.rect.left > 800:  # Ajustar a WIDTH si usas constante
            self.kill()
