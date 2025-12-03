import pygame, sys
from core.state import State
from settings import WIDTH, HEIGHT

class CreditsState(State):
    def __init__(self, game):
        super().__init__(game)

        # Cargar imagen de créditos
        self.image = pygame.image.load("assets/images/creditos.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        # Fuente para el mensaje "ENTER para volver"
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))

    def draw(self):
        # Mostrar imagen
        self.game.screen.blit(self.image, (0, 0))

        # Texto para regresar
        label = self.font.render("Presiona ENTER para volver", True, (255,255,255))
        self.game.screen.blit(label, label.get_rect(center=(WIDTH//2, HEIGHT - 50)))
