import pygame, sys
from settings import *
from core.state import State
import math  # Para el movimiento sinusoidal

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        # 1. CARGAR LA IMAGEN DE FONDO
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
        
        # NUEVO: Variables para movimiento del fondo (parallax simple horizontal)
        self.bg_x = 0  # Posición X del fondo
        self.scroll_speed = 0.5  # Velocidad de scroll (ajusta para más/menos movimiento)
        
        # NUEVO: Para oscilación del título (flotante)
        self.title_time = 0  # Contador para seno
        self.title_offset_y = 0  # Offset vertical dinámico
        self.title_y_base = 200  # Posición base Y del título

    def update(self):  # NUEVO: Método update para lógica de movimiento (llámalo en tu game loop)
        # Scroll del fondo (se mueve hacia la izquierda, seamless)
        self.bg_x -= self.scroll_speed
        if self.bg_x <= -self.background.get_width():
            self.bg_x = 0  # Reinicia para loop infinito
        
        # Oscilación del título (efecto flotante suave)
        self.title_time += 0.03  # Velocidad de oscilación (ajusta para más rápido/lento)
        self.title_offset_y = math.sin(self.title_time) * 8  # Amplitude de 8 píxeles

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
        # NUEVO: Dibujar fondo con scroll (doble blit para seamless)
        if self.background:
            # Blit primera copia
            self.game.screen.blit(self.background, (self.bg_x, 0))
            # Blit segunda copia para cubrir el hueco
            self.game.screen.blit(self.background, (self.bg_x + self.background.get_width(), 0))
            
            # --- OSCURECER EL FONDO UN POCO (Opcional) ---
            overlay = pygame.Surface((WIDTH, HEIGHT)) # Crear superficie negra
            overlay.set_alpha(120)  # Transparencia (0 a 255)
            overlay.fill((0, 0, 0))  # Color negro para oscurecer
            self.game.screen.blit(overlay, (0,0))
            # ---------------------------------------------
        else:
            self.game.screen.fill(COLOR_FONDO_OSCURO)

        # Título con oscilación (flotante)
        title = FONT_TITULO.render("Menú Principal", True, COLOR_BLANCO)
        title_rect = title.get_rect(center=(WIDTH//2, self.title_y_base + self.title_offset_y))
        self.game.screen.blit(title, title_rect)

        # Botones con efecto "neón"
        mx, my = pygame.mouse.get_pos()
        for text, y in self.buttons:
            rect = pygame.Rect(WIDTH//2 - 100, y - 25, 200, 50)
            # Efecto hover (cambia de color si el mouse está encima)
            is_hovered = rect.collidepoint(mx, my)
            color = COLOR_NEON_CIAN if is_hovered else COLOR_BLANCO
            
            label = FONT_MENU.render(text, True, color)
            self.game.screen.blit(label, label.get_rect(center=(WIDTH//2, y)))
