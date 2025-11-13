import pygame, sys
from settings import *
from core.state import State

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        # 1. CARGAR LA IMAGEN DE FONDO
        # Asegúrate de cambiar "menu_bg.png" por el nombre real de tu foto
        try:
            self.background = pygame.image.load("assets/images/intro2.png").convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except FileNotFoundError:
            print("No se encontró la imagen del menú. Se usará color sólido.")
            self.background = None  # Si falla, usaremos color normal
            
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
        if self.background:
            self.game.screen.blit(self.background, (0, 0))
            
            # --- OSCURECER EL FONDO UN POCO (Opcional) ---
            overlay = pygame.Surface((WIDTH, HEIGHT)) # Crear superficie negra
            overlay.set_alpha(120)  # Transparencia (0 a 255)
            self.game.screen.blit(overlay, (0,0))
            # ---------------------------------------------
        else:
            self.game.screen.fill(COLOR_FONDO_OSCURO)

        # Título
        title = FONT_TITULO.render("Menú Principal", True, COLOR_BLANCO)
        self.game.screen.blit(title, title.get_rect(center=(WIDTH//2, 200)))

        # Botones con efecto "neón"
        mx, my = pygame.mouse.get_pos()
        for text, y in self.buttons:
            rect = pygame.Rect(WIDTH//2 - 100, y - 25, 200, 50)
            # Efecto hover (cambia de color si el mouse está encima)
            is_hovered = rect.collidepoint(mx, my)
            color = COLOR_NEON_CIAN if is_hovered else COLOR_BLANCO
            
            label = FONT_MENU.render(text, True, color)
            self.game.screen.blit(label, label.get_rect(center=(WIDTH//2, y)))
