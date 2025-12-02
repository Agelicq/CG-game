import pygame, sys
from core.state import State
from settings import WIDTH, HEIGHT

class HelpState(State):
    def __init__(self, game):
        super().__init__(game)

        # Cargar imágenes de ayuda
        self.page = 0
        self.images = [
            pygame.image.load("assets/images/help1.png").convert_alpha(),
            pygame.image.load("assets/images/help2.png").convert_alpha()
        ]

        # Escalar a la pantalla
        self.images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in self.images]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                # Avanzar páginas con ENTER
                if event.key == pygame.K_RETURN:
                    self.page += 1
                    if self.page >= len(self.images):  # Si ya no hay más páginas → volver
                        from states.menu import MenuState
                        self.game.change_state(MenuState(self.game))

                # salir con ESC donde estés
                if event.key == pygame.K_ESCAPE:
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))


    def draw(self):
        self.game.screen.blit(self.images[self.page], (0, 0))

        font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 42)
        msg = "Presiona ENTER para continuar"
        label = font.render(msg, True, (255, 255, 255))

        # posición centrada abajo
        x = WIDTH // 2 + 20 
        y = HEIGHT - 560
        self.game.screen.blit(label, label.get_rect(center=(x, y)))
