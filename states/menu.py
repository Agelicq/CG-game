#!/usr/bin/env python3
"""Módulo del Menú Principal.

Este módulo contiene la clase MenuState que maneja la pantalla
principal del juego Astro Lost, incluyendo navegación entre
las diferentes opciones del menú.
"""

# Importaciones de librerías estándar
import math
import sys

# Importaciones de terceros
import pygame

# Importaciones locales
from settings import *
from core.state import State
from states.ayudaState import HelpState
from states.creditosState import CreditsState
from states.exit import ExitConfirmState


class MenuState(State):
    """Estado del menú principal del juego.
    
    Maneja la pantalla principal con opciones de navegación
    hacia diferentes secciones: jugar, puntajes, ayuda,
    créditos y salir del juego.
    
    Attributes:
        background: Imagen de fondo del menú o None si no se encuentra.
        buttons: Lista de tuplas (texto, posición_y) para los botones del menú.
    """
    def __init__(self, game):
        """Inicializa el estado del menú principal.
        
        Configura la imagen de fondo y define las opciones
        del menú con sus posiciones en pantalla.
        
        Args:
            game: Referencia al gestor principal del juego.
        """
        super().__init__(game)
        
        # === CONFIGURACIÓN DE FONDO ===
        try:
            # Cargar imagen de fondo del menú
            self.background = pygame.image.load("assets/images/menu.png").convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except FileNotFoundError:
            print("No se encontró la imagen del menú. Se usará color sólido.")
            self.background = None  # Fallback a color sólido
            
        # === CONFIGURACIÓN DE BOTONES ===
        # Lista de (texto_botón, posición_y)
        self.buttons = [
            ("Jugar", 150),
            ("Puntajes", 220),
            ("Ayuda", 290),
            ("Créditos", 360),
            ("Salir", 430)
        ]
        


    def handle_events(self):
        """Procesa los eventos de entrada del usuario.
        
        Maneja la salida del juego y la navegación por clic
        en los botones del menú, cambiando a los estados
        correspondientes según la opción seleccionada.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # === NAVEGACIÓN POR CLIC ===
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                
                # Verificar clic en cada botón
                for text, y in self.buttons:
                    rect = pygame.Rect(WIDTH//2 - 100, y - 25, 200, 50)
                    if rect.collidepoint(mx, my):
                        
                        if text == "Salir":
                            self.game.change_state(ExitConfirmState(self.game))
                        
                        elif text == "Jugar":
                            from states.input_name import InputNameState
                            self.game.change_state(InputNameState(self.game))

                        elif text == "Puntajes":
                            from states.scores import ScoreState
                            self.game.change_state(ScoreState(self.game))

                        elif text == "Ayuda":
                            self.game.change_state(HelpState(self.game))

                        elif text == "Créditos":
                            self.game.change_state(CreditsState(self.game))


    def draw(self):
        """Renderiza la interfaz del menú principal.
        
        Dibuja el fondo del menú con overlay oscuro opcional
        y los botones con efecto hover. Utiliza fuente temática
        para mantener la estética del juego.
        """
        # === RENDERIZADO DE FONDO ===
        if self.background:
            # Fondo estático (posición 0,0)
            self.game.screen.blit(self.background, (0, 0))

            # Overlay oscuro para mejorar legibilidad
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(120)  # Transparencia del 47%
            overlay.fill((0, 0, 0))
            self.game.screen.blit(overlay, (0, 0))
        else:
            # Fallback: fondo de color sólido
            self.game.screen.fill(COLOR_FONDO_OSCURO)

        # === RENDERIZADO DE BOTONES ===
        mx, my = pygame.mouse.get_pos()
        
        for text, y in self.buttons:
            rect = pygame.Rect(WIDTH//2 - 100, y - 25, 200, 50)
            
            # Efecto hover: cambio de color al pasar el mouse
            is_hovered = rect.collidepoint(mx, my)
            color = COLOR_NEON_CIAN if is_hovered else COLOR_BLANCO
            
            # Renderizar texto con fuente temática
            font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 45)
            label = font.render(text, True, color)
            self.game.screen.blit(label, label.get_rect(center=(WIDTH//2, y)))
