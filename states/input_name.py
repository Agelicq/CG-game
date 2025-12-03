#!/usr/bin/env python3
"""Módulo del Estado de Entrada de Nombre.

Este módulo contiene la clase InputNameState que maneja
la captura del nombre del jugador antes de comenzar
la selección de niveles.
"""

# Importaciones de librerías estándar
import sys

# Importaciones de terceros
import pygame

# Importaciones locales
from core.state import State
from settings import *


class InputNameState(State):
    """Estado de captura de nombre del jugador.
    
    Proporciona una interfaz para que el jugador ingrese
    su nombre antes de comenzar el juego, inicializando
    sus datos de progreso.
    
    Attributes:
        input_text: Cadena de texto que el jugador está escribiendo.
        font: Fuente utilizada para renderizar el texto.
    """

    def __init__(self, game):
        """Inicializa el estado de captura de nombre.
        
        Configura la fuente de texto y inicializa la
        cadena de entrada vacía.
        
        Args:
            game: Referencia al gestor principal del juego.
        """
        super().__init__(game)
        self.input_text = ""
        
        # === CONFIGURACIÓN DE FUENTE ===
        try:
            self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 50)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, 50)  # Fuente por defecto

    def handle_events(self):
        """Procesa los eventos de entrada del usuario.
        
        Captura la escritura del nombre, permite borrar caracteres
        con BACKSPACE y confirmar con ENTER para proceder al
        selector de niveles.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # === CONFIRMACIÓN Y CREACIÓN DE DATOS ===
                if event.key == pygame.K_RETURN:
                    if len(self.input_text) > 0:
                        # Crear estructura de datos del jugador
                        player_data = {
                            "name": self.input_text,
                            "total_time": 0.0,      # Tiempo acumulado
                            "levels_done": []       # Niveles completados
                        }

                        # Transición al selector de niveles
                        from states.level_select import LevelSelectState
                        self.game.change_state(LevelSelectState(self.game, player_data))
                
                # === BORRADO DE CARACTERES ===
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                
                # === ESCRITURA DE TEXTO ===
                else:
                    # Límite de 12 caracteres, solo caracteres imprimibles
                    if len(self.input_text) < 12 and event.unicode.isprintable():
                        self.input_text += event.unicode

    def update(self, dt=None):
        """Actualiza el estado de entrada de nombre.
        
        No requiere actualización de lógica, es una pantalla de entrada.
        
        Args:
            dt: Delta time (no utilizado).
        """
        pass

    def draw(self):
        """Renderiza la interfaz de captura de nombre.
        
        Muestra el título, instrucciones, campo de entrada
        y una caja visual alrededor del texto del jugador.
        """
        # === FONDO ===
        self.game.screen.fill(COLOR_FONDO_OSCURO)
        
        # === ELEMENTOS DE TEXTO ===
        title = self.font.render("IDENTIFICATE PILOTO", True, COLOR_BLANCO)
        prompt = self.font.render("Escribe tu nombre y presiona ENTER:", True, (150, 150, 150))
        name_surf = self.font.render(self.input_text, True, COLOR_NEON_CIAN)
        
        # === CÁLCULO DE POSICIONES CENTRADAS ===
        rect_title = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        rect_prompt = prompt.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        rect_name = name_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
        
        # === CAJA DE ENTRADA ===
        pygame.draw.rect(self.game.screen, COLOR_BLANCO, rect_name.inflate(40, 20), 2)
        
        # === RENDERIZADO DE ELEMENTOS ===
        self.game.screen.blit(title, rect_title)
        self.game.screen.blit(prompt, rect_prompt)
        self.game.screen.blit(name_surf, rect_name)