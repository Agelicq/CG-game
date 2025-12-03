#!/usr/bin/env python3
"""Cargador de Mapas del Juego.

Este módulo proporciona funciones para cargar mapas de niveles
desde archivos de texto para Astro Lost.
"""


def load_map(planet_name):
    """Carga un mapa de nivel desde un archivo de texto.
    
    Lee un archivo de texto que contiene la disposición del nivel
    y lo convierte en una matriz bidimensional de caracteres.
    Cada carácter representa un tipo diferente de tile o elemento.
    
    Args:
        planet_name (str): Nombre del planeta/nivel a cargar
        (glacius, volcanus, floria).
    Returns:
        list: Lista de listas donde cada sublista representa una fila
        del mapa y cada elemento es un carácter que representa
        un tipo de tile.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo del mapa.
        IOError: Si hay problemas al leer el archivo.
        
    Example:
        mapa = load_map("glacius")
        print(mapa[0])  # Primera fila del mapa
        ['#', '#', '#', '.', '.', 'P', '.', '#']
    """
    path = f"level/maps/{planet_name}.txt"
    
    with open(path, "r", encoding="utf-8") as archivo:
        # Leer todas las líneas y convertir cada una en lista de caracteres
        return [list(fila.strip()) for fila in archivo.readlines()]
