#!/usr/bin/env python3
"""Módulo del Estado de Ayuda.

Este módulo contiene la clase HelpState que muestra
las pantallas de ayuda con instrucciones del juego
en formato de páginas navegables.
"""

# Importaciones de librerías estándar
import sys

# Importaciones de terceros
import pygame

# Importaciones locales
from core.state import State
from settings import WIDTH, HEIGHT


class HelpState(State):
    """Estado de pantallas de ayuda del juego.
    
    Muestra una serie de imágenes instructivas que el
    jugador puede navegar con ENTER y salir con ESC.
    
    Attributes:
        page: Índice de la página actual de ayuda.
        images: Lista de imágenes de ayuda cargadas.
    """

    def __init__(self, game):
        """Inicializa el estado de ayuda.
        
        Carga y escala las imágenes de ayuda del juego.
        
        Args:
            game: Referencia al gestor principal del juego.
        """
        super().__init__(game)

        # === CONTROL DE NAVEGACIÓN ===
        self.page = 0
        
        # === CARGA DE IMÁGENES DE AYUDA ===
        self.images = [
            pygame.image.load("assets/images/help1.png").convert_alpha(),
            pygame.image.load("assets/images/help2.png").convert_alpha()
        ]

        # Escalar imágenes al tamaño de pantalla
        self.images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in self.images]

    def handle_events(self):
        """Procesa los eventos de entrada del usuario.
        
        Permite navegar entre páginas con ENTER y regresar
        al menú con ESC o al completar todas las páginas.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # === NAVEGACIÓN DE PÁGINAS ===
                if event.key == pygame.K_RETURN:
                    self.page += 1
                    # Si no hay más páginas, regresar al menú
                    if self.page >= len(self.images):
                        from states.menu import MenuState
                        self.game.change_state(MenuState(self.game))

                # === SALIDA DIRECTA AL MENÚ ===
                if event.key == pygame.K_ESCAPE:
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))

    def draw(self):
        """Renderiza la página actual de ayuda.
        
        Muestra la imagen de ayuda correspondiente y
        las instrucciones de navegación en pantalla.
        """
        # === IMAGEN DE AYUDA ACTUAL ===
        self.game.screen.blit(self.images[self.page], (0, 0))

        # === INSTRUCCIONES DE NAVEGACIÓN ===
        font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 42)
        msg = "Presiona ENTER para continuar"
        label = font.render(msg, True, (255, 255, 255))

        # Posicionamiento centrado en la parte inferior
        x = WIDTH // 2 + 20
        y = HEIGHT - 560
        self.game.screen.blit(label, label.get_rect(center=(x, y)))
