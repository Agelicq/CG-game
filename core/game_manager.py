# core/game_manager.py
import pygame, sys
from settings import *
from states.intro import IntroState

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Astro Lost")
        self.clock = pygame.time.Clock()
        self.state = IntroState(self)  # Estado inicial

    def change_state(self, new_state):
        self.state = new_state

    def run(self):
        while True:
            self.state.handle_events()
            self.state.update()
            self.state.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
