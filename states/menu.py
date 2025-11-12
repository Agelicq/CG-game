import pygame, sys
from settings import *
from core.state import State

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            ("Jugar", 250),
            ("Puntajes", 320),
            ("Ayuda", 390),
            ("Créditos", 460),
            ("Salir", 530)
        ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                for text, y in self.buttons:
                    rect = pygame.Rect(WIDTH//2 - 100, y - 25, 200, 50)
                    if rect.collidepoint(mx, my):
                        if text == "Salir":
                            pygame.quit(); sys.exit()
                        elif text == "Jugar":
                            print("Ir a selección de nivel (pendiente)")
                        else:
                            print(f"Abrir {text} (pendiente)")

    def draw(self):
        self.game.screen.fill(COLOR_FONDO_OSCURO)

        # Título
        title = FONT_TITULO.render("Menú Principal", True, COLOR_BLANCO)
        self.game.screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))

        # Botones con efecto "neón"
        mx, my = pygame.mouse.get_pos()
        for text, y in self.buttons:
            rect = pygame.Rect(WIDTH//2 - 100, y - 25, 200, 50)
            color = COLOR_NEON_CIAN if rect.collidepoint(mx, my) else COLOR_BLANCO
            label = FONT_MENU.render(text, True, color)
            self.game.screen.blit(label, label.get_rect(center=(WIDTH//2, y)))
