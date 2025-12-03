import pygame, sys
from core.state import State
from settings import WIDTH, HEIGHT

class ExitConfirmState(State):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 40)

        # Botones
        self.buttons = {
            "yes": pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 40, 120, 50),
            "no": pygame.Rect(WIDTH//2 + 30, HEIGHT//2 + 40, 120, 50)
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # ---------- CLICK DEL MOUSE ----------
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()

                if self.buttons["yes"].collidepoint(mx, my):
                    pygame.quit(); sys.exit()

                if self.buttons["no"].collidepoint(mx, my):
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))

            # ---------- TECLAS OPCIONALES ----------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit(); sys.exit()

                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))

    def draw(self):
        # Fondo oscurecido
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.game.screen.blit(overlay, (0, 0))

        # Ventana
        box_w, box_h = 600, 200
        box_rect = pygame.Rect(
            (WIDTH - box_w)//2,
            (HEIGHT - box_h)//2,
            box_w, box_h
        )
        pygame.draw.rect(self.game.screen, (10,10,10), box_rect)
        pygame.draw.rect(self.game.screen, (0,255,255), box_rect, 3)

        # Texto
        title = self.font.render("CONFIRMAR SALIDA DEL JUEGO?", True, (255,255,255))
        self.game.screen.blit(title, title.get_rect(center=(WIDTH//2, box_rect.y + 55)))

        # Dibujar botones
        mx, my = pygame.mouse.get_pos()
        for name, rect in self.buttons.items():
            hovered = rect.collidepoint(mx, my)
            color = (0,255,255) if hovered else (255,255,255)

            pygame.draw.rect(self.game.screen, (20,20,20), rect)
            pygame.draw.rect(self.game.screen, color, rect, 2)

            label_text = "Sí" if name == "yes" else "No"
            label = self.font.render(label_text, True, color)
            self.game.screen.blit(label, label.get_rect(center=rect.center))
