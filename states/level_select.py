#!/usr/bin/env python3
"""Módulo del Selector de Niveles.

Este módulo contiene la clase LevelSelectState que maneja
la selección de planetas/niveles, mostrando el progreso
del jugador y permitiendo acceder a los diferentes mundos.
"""

# Importaciones de librerías estándar
import sys

# Importaciones de terceros
import pygame

# Importaciones locales
from core.state import State
from settings import *
from states.gamePlayState import GameplayState
from states.victory import VictoryState


class LevelSelectState(State):
    """Estado del selector de niveles/planetas.
    
    Presenta una interfaz visual para seleccionar entre
    los diferentes planetas disponibles, mostrando el
    progreso completado y verificando condiciones de victoria.
    
    Attributes:
        player_data: Datos del progreso del jugador.
        background: Imagen de fondo del selector.
        planet_glacius: Imagen del planeta Glacius.
        planet_volcanus: Imagen del planeta Volcanus.
        planet_floria: Imagen del planeta Floria.
        sound_select: Sonido de selección de planeta.
        sound_volume: Volumen del sonido de selección.
        sound_max_ms: Duración máxima del sonido.
        sound_fade_ms: Tiempo de fade del sonido.
        positions: Posiciones de los planetas en pantalla.
        base_size: Tamaño base de los planetas.
        hover_size: Tamaño de los planetas al hacer hover.
    """
    def __init__(self, game, player_data):
        """Inicializa el selector de niveles.
        
        Carga las imágenes de los planetas, configura el fondo
        y establece las propiedades de sonido y posicionamiento.
        
        Args:
            game: Referencia al gestor principal del juego.
            player_data (dict): Datos del progreso del jugador.
        """
        super().__init__(game)
        self.player_data = player_data
        
        # === CONFIGURACIÓN DE FONDO ===
        try:
            self.background = pygame.image.load("assets/images/BGgame_select.png").convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except FileNotFoundError:
            # Fallback: fondo negro si no se encuentra la imagen
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((0, 0, 0))

        # === CARGA DE IMÁGENES DE PLANETAS ===
        self.planet_glacius = pygame.image.load("assets/images/glacius.png").convert_alpha()
        self.planet_volcanus = pygame.image.load("assets/images/volcanus.png").convert_alpha()
        self.planet_floria = pygame.image.load("assets/images/floria.png").convert_alpha()

        # === CONFIGURACIÓN DE AUDIO ===
        self.sound_select = pygame.mixer.Sound("assets/music/rocket.mp3")
        self.sound_volume = 0.4      # Volumen moderado
        self.sound_max_ms = 700      # Duración máxima: 0.7s
        self.sound_fade_ms = 0       # Sin fade
        self.sound_select.set_volume(self.sound_volume)

        # === POSICIONAMIENTO DE PLANETAS ===
        self.positions = {
            "glacius": (200, 320),   # Planeta izquierdo
            "volcanus": (400, 320),  # Planeta central
            "floria": (600, 320)     # Planeta derecho
        }
        
        # === TAMAÑOS DE PLANETAS ===
        self.base_size = 130    # Tamaño normal
        self.hover_size = 150   # Tamaño al hacer hover

    def update(self, dt=None):
        """Verifica las condiciones de victoria del juego.
        
        Comprueba si el jugador ha completado todos los planetas
        para activar la secuencia de victoria y guardar puntaje.
        
        Args:
            dt: Delta time (no utilizado en este método).
        """
        total_planetas = 3  # Número total de planetas en el juego
        
        # Verificar si se completaron todos los planetas
        if len(self.player_data["levels_done"]) >= total_planetas:
            self.save_score_and_finish()

    def save_score_and_finish(self):
        """Calcula el tiempo, guarda y lanza la VICTORIA"""
        
        total_seconds = int(self.player_data["total_time"])
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_str = f"{minutes:02}:{seconds:02}"
        name = self.player_data["name"]

        print(f"¡JUEGO COMPLETADO! {name} Time :{time_str} min")

        # Guardar en TXT
        try:
            with open("puntajes_totales.txt", "a") as f:
                f.write(f"{name} Time :{time_str} min\n")
        except Exception as e:
            print("Error guardando:", e)
        
        # --- CAMBIO: IR A PANTALLA DE VICTORIA ---
        self.game.change_state(VictoryState(self.game, name, time_str))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from states.menu import MenuState
                self.game.change_state(MenuState(self.game))
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                for name, (x, y) in self.positions.items():
                    planet_rect = pygame.Rect(x - self.hover_size//2, y - self.hover_size//2, self.hover_size, self.hover_size)
                    
                    if planet_rect.collidepoint((mx, my)):
                        if name in self.player_data["levels_done"]:
                            print("¡Ya completaste este planeta!")
                        else:
                            # Reproducir sonido
                            self.sound_select.play(maxtime=self.sound_max_ms, fade_ms=self.sound_fade_ms)
                            # Ir al juego
                            self.game.change_state(GameplayState(self.game, name, self.player_data))

    def draw(self):
        """Renderiza la interfaz del selector de niveles.
        
        Dibuja el fondo, los planetas con efectos visuales
        de hover y transparencia para mostrar progreso,
        y los nombres de los planetas con colores indicativos.
        """
        screen = self.game.screen
        
        # === FONDO ===
        screen.blit(self.background, (0, 0))

        # Obtener posición del mouse para efectos hover
        mx, my = pygame.mouse.get_pos()

        # === RENDERIZADO DE PLANETAS ===
        for name, (x, y) in self.positions.items():
            img = getattr(self, f"planet_{name}")
            
            # Efecto visual: transparencia para planetas completados
            if name in self.player_data["levels_done"]:
                img.set_alpha(100)  # Transparente (completado)
            else:
                img.set_alpha(255)  # Opaco (disponible)

            # Área de detección para hover
            distance_rect = pygame.Rect(
                x - self.base_size//2, 
                y - self.base_size//2, 
                self.base_size, 
                self.base_size
            )

            # Efecto hover: agrandar planeta al pasar mouse
            if distance_rect.collidepoint((mx, my)):
                img_scaled = pygame.transform.scale(img, (self.hover_size, self.hover_size))
            else:
                img_scaled = pygame.transform.scale(img, (self.base_size, self.base_size))

            # Centrar y dibujar planeta
            rect = img_scaled.get_rect(center=(x, y))
            screen.blit(img_scaled, rect)

        # === CONFIGURACIÓN DE FUENTE ===
        try:
            font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 35)
        except FileNotFoundError:
            font = pygame.font.SysFont("verdana", 35)  # Fallback

        # === NOMBRES DE PLANETAS ===
        nombres = [("glacius", 200), ("volcanus", 400), ("floria", 600)]
        
        for txt, x_pos in nombres:
            # Color indicativo: verde (completado) o blanco (disponible)
            color = (0, 255, 0) if txt in self.player_data["levels_done"] else (255, 255, 255)
            
            text_surf = font.render(txt, True, color)
            screen.blit(text_surf, text_surf.get_rect(center=(x_pos, 410)))