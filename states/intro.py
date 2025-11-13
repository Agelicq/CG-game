# states/intro.py
import pygame, time, sys
from settings import *
from core.state import State
from states.menu import MenuState


    
class IntroState(State):
    def __init__(self, game):
        super().__init__(game)
        self.start_time = time.time()
        self.duration = 3  # segundos
        self.transition_done = False

        # 🔹 Carga la imagen
        self.background = pygame.image.load("assets/images/intro2.png").convert()
        # 🔹 Ajusta la imagen al tamaño de la pantalla
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self._to_menu()

    def update(self):
        if not self.transition_done and time.time() - self.start_time > self.duration:
            self._to_menu()

    def _to_menu(self):
        if not self.transition_done:
            self.transition_done = True
            self.game.change_state(MenuState(self.game))

    def draw(self):
        # Dibuja la imagen completa
        self.game.screen.blit(self.background, (0, 0))
