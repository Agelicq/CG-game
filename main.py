#!/usr/bin/env python3
"""Módulo Principal del Juego Astro Lost.

Este módulo contiene el punto de entrada principal del juego.
Inicializa el GameManager y ejecuta el bucle principal del juego.

El juego Astro Lost es un plataformero 2D donde el jugador controla
un astro-bot que debe recuperar fragmentos de energía en diferentes
planetas para completar su misión espacial.
"""

# Importaciones locales
from core.game_manager import GameManager


def main():
    """Función principal del juego.
    
    Inicializa el gestor del juego y ejecuta el bucle principal.
    Esta función sirve como punto de entrada limpio y permite
    mejor manejo de errores y testing.
    """
    game = GameManager()
    game.run()


if __name__ == "__main__":
    main()
