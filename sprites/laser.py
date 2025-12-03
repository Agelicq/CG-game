
"""Módulo de Láseres del Juego.

Este módulo contiene la clase Laser que representa
obstáculos de láser que se activan y desactivan
periódicamente en Astro Lost.
"""

import pygame
import time


class Laser(pygame.sprite.Sprite):
    """Clase que representa un láser peligroso en el juego.
    
    Los láseres son obstáculos que se activan y desactivan
    en intervalos regulares, dañando al jugador cuando están activos.
    
    Atributos:
        x (int): Coordenada X del láser.
        y (int): Coordenada Y del láser.
        length (int): Longitud del láser en píxeles.
        interval (float): Intervalo en segundos entre activación/desactivación.
        active (bool): Estado actual del láser (activo/inactivo).
        timer (float): Temporizador interno para controlar intervalos.
    """
    
    def __init__(self, x, y, length, interval=2):
        """Inicializa un nuevo láser.
        
        Args:
            x (int): Coordenada X de la posición del láser.
            y (int): Coordenada Y de la posición del láser.
            length (int): Longitud del láser en píxeles.
            interval (float): Segundos entre encendido y apagado.
            Por defecto 2 segundos.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.length = length
        self.interval = interval  # Segundos ENCENDIDO / APAGADO
        self.active = False
        self.timer = 0

    def update(self, dt, player):
        """Actualiza el estado del láser y verifica colisiones.
        
        Args:
            dt (float): Tiempo transcurrido desde la última actualización.
            player (Player): Instancia del jugador para verificar colisiones.
        """
        # Actualizar temporizador
        self.timer += dt
        if self.timer >= self.interval:
            self.timer = 0
            self.active = not self.active  # Alternar estado

        # Verificar colisión con el jugador si está activo
        if self.active:
            laser_rect = pygame.Rect(self.x, self.y, 6, self.length)
            if laser_rect.colliderect(player.rect):
                player.take_damage(10)   # Daño por contacto

    def draw(self, surface):
        """Dibuja el láser en la superficie si está activo.
        
        Args:
            surface (pygame.Surface): Superficie donde dibujar el láser.
        """
        if self.active:
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 3, self.length))
