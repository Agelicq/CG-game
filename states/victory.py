#!/usr/bin/env python3
"""Módulo del Estado de Victoria.

Este módulo contiene la clase VictoryState que maneja
la pantalla de celebración cuando el jugador completa
todos los niveles del juego.
"""

# Importaciones de librerías estándar
import sys

# Importaciones de terceros
import pygame

# Importaciones locales
from core.state import State
from settings import *


class VictoryState(State):
    """Estado de pantalla de victoria.
    
    Muestra una pantalla de celebración con el tiempo final
    del jugador cuando completa todos los niveles del juego.
    
    Attributes:
        name: Nombre del jugador que completó el juego.
        time: Tiempo total empleado para completar todos los niveles.
        font_big: Fuente grande para el título principal.
        font_small: Fuente pequeña para información adicional.
        bg: Imagen de fondo de la pantalla de victoria.
    """
    def __init__(self, game, player_name, final_time):
        """Inicializa el estado de victoria.
        
        Configura las fuentes y el fondo para mostrar
        la información de victoria del jugador.
        
        Args:
            game: Referencia al gestor principal del juego.
            player_name (str): Nombre del jugador ganador.
            final_time: Tiempo total empleado para completar el juego.
        """
        super().__init__(game)
        self.name = player_name
        self.time = final_time
        
        # === CONFIGURACIÓN DE FUENTES ===
        try:
            self.font_big = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 80)
            self.font_small = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 50)
        except FileNotFoundError:
            # Fallback: fuentes del sistema
            self.font_big = pygame.font.SysFont("Arial", 60, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 40)
            
        # === CONFIGURACIÓN DE FONDO ===
        try:
            self.bg = pygame.image.load("assets/images/bgpuntajes.png").convert()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except FileNotFoundError:
            # Fallback: fondo verde sólido
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((20, 100, 40))  # Verde oscuro temático

    def handle_events(self):
        """Procesa los eventos de entrada del usuario.
        
        Permite salir del juego o regresar al menú principal
        con cualquier tecla o clic del mouse.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # === REGRESO AL MENÚ ===
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                from states.menu import MenuState
                self.game.change_state(MenuState(self.game))

    def update(self, dt=None):
        """Actualiza el estado de victoria.
        
        No requiere actualización de lógica, es una pantalla estática.
        
        Args:
            dt: Delta time (no utilizado).
        """
        pass

    def draw(self):
        """Renderiza la pantalla de victoria.
        
        Muestra el fondo temático y los textos de celebración
        con la información del jugador y su tiempo final.
        """
        # === FONDO ===
        self.game.screen.blit(self.bg, (0, 0))
        
        # === CÁLCULO DE POSICIONES CENTRADAS ===
        cx, cy = WIDTH // 2, HEIGHT // 2
        
        # === RENDERIZADO DE TEXTOS ===
        # Título principal (dorado)
        txt_title = self.font_big.render("¡MISION CUMPLIDA!", True, (255, 215, 0))
        
        # Información del jugador (blanco)
        txt_name = self.font_small.render(f"Piloto: {self.name}", True, (255, 255, 255))
        txt_time = self.font_small.render(f"Tiempo Total: {self.time} min", True, (255, 255, 255))
        
        # Instrucción de continuación (gris claro)
        txt_press = self.font_small.render("Presiona para continuar...", True, (200, 200, 200))

        # === POSICIONAMIENTO DE TEXTOS ===
        self.game.screen.blit(txt_title, txt_title.get_rect(center=(cx, cy - 80)))
        self.game.screen.blit(txt_name, txt_name.get_rect(center=(cx, cy)))
        self.game.screen.blit(txt_time, txt_time.get_rect(center=(cx, cy + 50)))
        self.game.screen.blit(txt_press, txt_press.get_rect(center=(cx, HEIGHT - 50)))