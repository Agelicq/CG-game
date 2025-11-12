import pygame, time, sys
from settings import *
from core.state import State
from states.menu import MenuState  # Importamos el siguiente estado

class IntroState(State):
    def __init__(self, game):
        super().__init__(game)
        self.start_time = time.time()
        self.duration = 3  # segundos
        self.transition_done = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                # Si el jugador hace clic o presiona una tecla, saltamos la intro
                self._to_menu()

    def update(self):
        if not self.transition_done and time.time() - self.start_time > self.duration:
            self._to_menu()

    def _to_menu(self):
        """Cambia al menú principal una sola vez."""
        if not self.transition_done:
            self.transition_done = True
            self.game.change_state(MenuState(self.game))

    def draw(self):
        self.game.screen.fill(COLOR_FONDO_OSCURO)

        # Texto principal
        text = FONT_TITULO.render("Astro Lost", True, COLOR_BLANCO)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.game.screen.blit(text, rect)

        # Texto auxiliar
        sub = FONT_MENU.render("Clic o tecla para continuar", True, COLOR_NEON_CIAN)
        sub_rect = sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
        self.game.screen.blit(sub, sub_rect)
