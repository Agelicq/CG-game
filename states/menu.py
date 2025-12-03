import pygame, sys
from settings import *
from core.state import State
from states.ayudaState import HelpState
from states.creditosState import CreditsState
from states.exit import ExitConfirmState
import math  

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        # 1. CARGAR LA IMAGEN DE FONDO
        try:
            self.background = pygame.image.load("assets/images/menu.png").convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except FileNotFoundError:
            print("No se encontró la imagen del menú. Se usará color sólido.")
            self.background = None  # Si falla, usaremos color normal
            
        self.buttons = [
            ("Jugar", 150),
            ("Puntajes", 220),
            ("Ayuda", 290),
            ("Créditos", 360),
            ("Salir", 430)
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
                            self.game.change_state(ExitConfirmState(self.game))
                        
                        elif text == "Jugar":
                            from states.input_name import InputNameState
                            self.game.change_state(InputNameState(self.game))

                        elif text == "Puntajes":
                            print("Mostrar puntajes (pendiente)")

                        elif text == "Ayuda":
                            self.game.change_state(HelpState(self.game))


                        elif text == "Créditos":
                            self.game.change_state(CreditsState(self.game))


    def draw(self):
        # Fondo estático (blit único en 0,0)
        if self.background:
            self.game.screen.blit(self.background, (0, 0))

            # --- OSCURECER EL FONDO UN POCO (Opcional) ---
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            self.game.screen.blit(overlay, (0, 0))
            # ---------------------------------------------
        else:
            self.game.screen.fill(COLOR_FONDO_OSCURO)

        # Botones con efecto "neón"
        mx, my = pygame.mouse.get_pos()
        for text, y in self.buttons:
            rect = pygame.Rect(WIDTH//2 - 100, y - 25, 200, 50)
            # Efecto hover (cambia de color si el mouse está encima)
            is_hovered = rect.collidepoint(mx, my)
            color = COLOR_NEON_CIAN if is_hovered else COLOR_BLANCO
            font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 45)
            label = font.render(text, True, color)
            self.game.screen.blit(label, label.get_rect(center=(WIDTH//2, y)))
