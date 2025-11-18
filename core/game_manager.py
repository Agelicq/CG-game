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
            # Eventos
            self.state.handle_events()

            # Delta time en segundos (útil para actualizaciones basadas en tiempo)
            dt_ms = self.clock.tick(FPS)
            dt = dt_ms / 1000.0

            # Llamar a update pasando dt cuando el método lo acepte.
            try:
                self.state.update(dt)
            except TypeError:
                # Compatibilidad con estados que no esperan dt
                self.state.update()

            # Dibujado
            self.state.draw()
            pygame.display.flip()
