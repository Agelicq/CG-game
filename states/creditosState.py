#!/usr/bin/env python3
"""Módulo del Estado de Créditos.

Este módulo contiene la clase CreditsState que muestra
la pantalla de créditos del juego con información
sobre los desarrolladores y recursos utilizados.
"""

# Importaciones de librerías estándar
import sys

# Importaciones de terceros
import pygame

# Importaciones locales
from core.state import State
from settings import WIDTH, HEIGHT


class CreditsState(State):
    """Estado de pantalla de créditos.
    
    Muestra una imagen con la información de créditos
    del juego, permitiendo regresar al menú con ENTER o ESC.
    
    Attributes:
        image: Imagen de créditos escalada al tamaño de pantalla.
        font: Fuente para el mensaje de navegación.
    """

    def __init__(self, game):
        """Inicializa el estado de créditos.
        
        Carga y escala la imagen de créditos y configura
        la fuente para el mensaje de navegación.
        
        Args:
            game: Referencia al gestor principal del juego.
        """
        super().__init__(game)

        # === CARGA DE IMAGEN DE CRÉDITOS ===
        self.image = pygame.image.load("assets/images/creditos.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        # === CONFIGURACIÓN DE FUENTE ===
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 40)

    def handle_events(self):
        """Procesa los eventos de entrada del usuario.
        
        Permite salir del juego o regresar al menú principal
        con las teclas ENTER o ESC.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # === REGRESO AL MENÚ ===
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))

    def draw(self):
        """Renderiza la pantalla de créditos.
        
        Muestra la imagen de créditos y el mensaje de
        navegación en la parte inferior de la pantalla.
        """
        # === IMAGEN DE CRÉDITOS ===
        self.game.screen.blit(self.image, (0, 0))

        # === MENSAJE DE NAVEGACIÓN ===
        label = self.font.render("Presiona ENTER para volver", True, (255, 255, 255))
        self.game.screen.blit(label, label.get_rect(center=(WIDTH//2, HEIGHT - 50)))
