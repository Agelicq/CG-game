#!/usr/bin/env python3
"""Módulo del Estado de Game Over.

Este módulo contiene la clase GameOverState que maneja
la pantalla que se muestra cuando el jugador pierde,
permitiendo regresar al menú principal.
"""

# Importaciones de terceros
import pygame

# Importaciones locales
from settings import *


class GameOverState:
    """Estado de fin de juego por derrota.
    
    Muestra una pantalla de Game Over cuando el jugador
    pierde y permite regresar al menú principal presionando ENTER.
    
    Attributes:
        game: Referencia al gestor principal del juego.
        background: Imagen de fondo de la pantalla Game Over.
    """
    def __init__(self, game):
        """Inicializa el estado de Game Over.
        
        Carga la imagen de fondo de la pantalla de derrota
        y la escala al tamaño de la pantalla.
        
        Args:
            game: Referencia al gestor principal del juego.
        """
        self.game = game
        
        # === CONFIGURACIÓN DE FONDO ===
        self.background = pygame.image.load("assets/images/gameOver.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def handle_events(self):
        """Procesa los eventos de entrada del usuario.
        
        Maneja la salida del juego y permite regresar al
        menú principal presionando la tecla ENTER.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            # === REGRESO AL MENÚ ===
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    import states.menu as menu
                    self.game.change_state(menu.MenuState(self.game))

    def update(self, dt=0):
        """Actualiza el estado de Game Over.
        
        No requiere actualización de lógica, es una pantalla estática.
        
        Args:
            dt: Delta time (no utilizado).
        """
        pass

    def draw(self):
        """Renderiza la pantalla de Game Over.
        
        Dibuja la imagen de fondo con un overlay oscuro
        para crear el efecto visual apropiado para la derrota.
        """
        if self.background:
            # === FONDO DE GAME OVER ===
            self.game.screen.blit(self.background, (0, 0))
            
            # === OVERLAY OSCURO ===
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(120)  # Transparencia del 47%
            overlay.fill((0, 0, 0))
            self.game.screen.blit(overlay, (0, 0))
