import pygame
import sys
from core.state import State
from settings import *

class LevelSelectState(State):
    def __init__(self, game):
        super().__init__(game)

        # Fondo espacial
        self.background = pygame.image.load("assets/images/BGgame_select.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Imágenes de los planetas (con transparencia)
        self.planet_glacius = pygame.image.load("assets/images/glacius.png").convert_alpha()
        self.planet_volcanus = pygame.image.load("assets/images/volcanus.png").convert_alpha()
        self.planet_floria = pygame.image.load("assets/images/floria.png").convert_alpha()

        # Sonido al seleccionar planeta
        self.sound_select = pygame.mixer.Sound("assets/music/rocket.mp3")
        # Parámetros de audio 
        self.sound_volume = 0.4       # rango 0.0 - 1.0
        self.sound_max_ms = 1000      # duración máxima en ms (maxtime)
        self.sound_fade_ms = 0        # fade-in en ms al reproducir
        # Aplicar volumen inicial
        self.sound_select.set_volume(self.sound_volume)

        # Posiciones (centros)
        self.positions = {
            "glacius": (200, 320),
            "volcanus": (400, 320),
            "floria": (600, 320)
        }

        # Escala base
        self.base_size = 130
        self.hover_size = 150

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
                        # Asegurar volumen configurado y reproducir con duración máxima
                        self.sound_select.set_volume(self.sound_volume)
                        # maxtime limita la reproducción a self.sound_max_ms milisegundos
                        self.sound_select.play(maxtime=self.sound_max_ms, fade_ms=self.sound_fade_ms)
                        print(f"Cargando planeta: {name}")
                        # Aquí después irá el cambio al gameplay

                        # Aquí cambiarías al gameplay
                        # from states.gameplay import GameplayState
                        # self.game.change_state(GameplayState(self.game, name))

    def update(self, dt=None):
        # Actualmente no usamos dt aquí, pero lo aceptamos para compatibilidad
        return

    def draw(self):
        screen = self.game.screen
        screen.blit(self.background, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # Dibujar planetas con efecto hover (escala)
        for name, (x, y) in self.positions.items():
            img = getattr(self, f"planet_{name}")
            distance_rect = pygame.Rect(x - self.base_size//2, y - self.base_size//2, self.base_size, self.base_size)

            if distance_rect.collidepoint((mx, my)):
                img_scaled = pygame.transform.scale(img, (self.hover_size, self.hover_size))
            else:
                img_scaled = pygame.transform.scale(img, (self.base_size, self.base_size))

            rect = img_scaled.get_rect(center=(x, y))
            screen.blit(img_scaled, rect)

        # Título
        try:
            font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 35)
        except Exception:
                font = pygame.font.SysFont("verdana", 35)

        text = font.render("glacius", True, COLOR_BLANCO)
        screen.blit(text, text.get_rect(center=(200, 410)))

        text = font.render("volcanus", True, COLOR_BLANCO)
        screen.blit(text, text.get_rect(center=(400, 410)))

        text = font.render("floria", True, COLOR_BLANCO)
        screen.blit(text, text.get_rect(center=(600, 410)))