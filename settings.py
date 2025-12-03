#!/usr/bin/env python3
"""Configuraciones Globales del Juego Astro Lost.

Este módulo contiene todas las constantes y configuraciones
globales utilizadas a lo largo del juego, incluyendo resolución,
colores temáticos y configuraciones de rendimiento.
"""

# Importaciones de terceros
import pygame

# === CONFIGURACIÓN DE PANTALLA ===
WIDTH = 800   # Ancho de la ventana en píxeles
HEIGHT = 600  # Alto de la ventana en píxeles
FPS = 60      # Frames por segundo objetivo

# === PALETA DE COLORES TEMÁTICOS ===
# Colores diseñados para crear una atmósfera espacial
COLOR_FONDO_OSCURO = (5, 0, 20)      # Azul muy oscuro (espacio profundo)
COLOR_BLANCO = (230, 230, 250)       # Blanco ligeramente azulado
COLOR_NEON_CIAN = (0, 255, 255)      # Cian brillante (elementos interactivos)

# === INICIALIZACIÓN DE PYGAME ===
# Inicializar el sistema de fuentes para uso global
pygame.font.init()

