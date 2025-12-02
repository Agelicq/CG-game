import pygame, sys
from core.state import State
from settings import *


class VictoryState(State):
    def __init__(self, game, player_name, final_time):
        super().__init__(game)
        self.name = player_name
        self.time = final_time
        
        # Cargar fuente
        try:
            self.font_big = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 80)
            self.font_small = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 50)
        except:
            self.font_big = pygame.font.SysFont("Arial", 60, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 40)
            
        # Cargar fondo de victoria (opcional, si no hay usa verde)
        try:
            self.bg = pygame.image.load("assets/images/victory.png").convert()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((20, 100, 40)) # Verde oscuro

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            # Al hacer clic o tecla, vuelve al MENU
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                from states.menu import MenuState
                self.game.change_state(MenuState(self.game))

    def update(self, dt=None):
        pass

    def draw(self):
        self.game.screen.blit(self.bg, (0, 0))
        
        # Textos centrados
        cx, cy = WIDTH // 2, HEIGHT // 2
        
        txt_title = self.font_big.render("¡MISION CUMPLIDA!", True, (255, 215, 0))
        txt_name = self.font_small.render(f"Piloto: {self.name}", True, (255, 255, 255))
        txt_time = self.font_small.render(f"Tiempo Total: {self.time} min", True, (255, 255, 255))
        txt_press = self.font_small.render("Presiona para continuar...", True, (200, 200, 200))

        self.game.screen.blit(txt_title, txt_title.get_rect(center=(cx, cy - 80)))
        self.game.screen.blit(txt_name, txt_name.get_rect(center=(cx, cy)))
        self.game.screen.blit(txt_time, txt_time.get_rect(center=(cx, cy + 50)))
        self.game.screen.blit(txt_press, txt_press.get_rect(center=(cx, HEIGHT - 50)))