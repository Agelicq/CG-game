import pygame
from settings import *
class GameOverState:
    def __init__(self, game):
        self.game = game
        self.background = pygame.image.load("assets/images/gameOver.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER para volver al menú
                    import states.menu as menu
                    self.game.change_state(menu.MenuState(self.game))


    def update(self, dt=0):
        pass

    def draw(self):
        if self.background:
            self.game.screen.blit(self.background, (0, 0))
        #oscurece el fondo
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            self.game.screen.blit(overlay, (0, 0))
