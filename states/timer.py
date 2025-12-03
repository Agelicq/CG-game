#!/usr/bin/env python3
"""Módulo del Temporizador de Juego.

Este módulo contiene la clase GameTimer que proporciona
funcionalidad de cronometraje visual para mostrar el
tiempo transcurrido durante el gameplay.
"""

# Importaciones de librerías estándar
import time

# Importaciones de terceros
import pygame

# Importaciones locales
from settings import WIDTH


class GameTimer:
    """Temporizador visual para el juego.
    
    Proporciona un cronometro que muestra el tiempo transcurrido
    en formato MM:SS en la esquina superior derecha de la pantalla
    con efecto de sombra para mejorar la legibilidad.
    
    Attributes:
        font: Fuente utilizada para renderizar el texto del tiempo.
        color_text: Color del texto principal (blanco).
        color_shadow: Color de la sombra del texto (negro).
    """

    def __init__(self):
        """Inicializa el temporizador del juego.
        
        Configura la fuente temática y los colores para
        el renderizado del cronometro.
        """
        # === CONFIGURACIÓN DE FUENTE ===
        try:
            self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 45)
        except FileNotFoundError:
            # Fallback: fuente del sistema
            self.font = pygame.font.SysFont("Consolas", 35, bold=True)
            
        # === CONFIGURACIÓN DE COLORES ===
        self.color_text = (255, 255, 255)    # Blanco para el texto
        self.color_shadow = (0, 0, 0)        # Negro para la sombra

    def draw(self, screen, start_time):
        """Renderiza el temporizador en pantalla.
        
        Calcula el tiempo transcurrido desde start_time y lo
        muestra en formato MM:SS en la esquina superior derecha
        con efecto de sombra.
        
        Args:
            screen: Superficie de pygame donde dibujar.
            start_time: Tiempo de inicio en segundos (time.time()).
        """
        # === CÁLCULO DE TIEMPO TRANSCURRIDO ===
        current_time = time.time()
        elapsed = int(current_time - start_time)
        
        # === FORMATEO A MM:SS ===
        minutes = elapsed // 60
        seconds = elapsed % 60
        time_str = f"TIME {minutes:02}:{seconds:02}"
        
        # === RENDERIZADO DE SUPERFICIES ===
        text_surf = self.font.render(time_str, True, self.color_text)
        shadow_surf = self.font.render(time_str, True, self.color_shadow)
        
        # === CÁLCULO DE POSICIÓN (esquina superior derecha) ===
        x = screen.get_width() - text_surf.get_width() - 20
        y = 20  # Margen superior
        
        # === RENDERIZADO CON EFECTO SOMBRA ===
        screen.blit(shadow_surf, (x + 2, y + 2))  # Sombra desplazada
        screen.blit(text_surf, (x, y))            # Texto principal