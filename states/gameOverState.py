import pygame

class GameOverState:
    def __init__(self, game):
        self.game = game
        self.font_big = pygame.font.Font(None, 80)
        self.font_small = pygame.font.Font(None, 40)

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
        self.game.screen.fill((0, 0, 0))
        text = self.font_big.render("GAME OVER", True, (255, 0, 0))
        text2 = self.font_small.render("Presiona ENTER para continuar", True, (255, 255, 255))

        rect = text.get_rect(center=(400, 250))
        rect2 = text2.get_rect(center=(400, 350))

        self.game.screen.blit(text, rect)
        self.game.screen.blit(text2, rect2)
