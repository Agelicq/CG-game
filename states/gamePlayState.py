import pygame
import sys
from core.state import State
from level.level import Level

class GameplayState(State):
    def __init__(self, game, planet_name):
        super().__init__(game)
        self.planet = planet_name
        self.level = Level(planet_name)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from states.level_select import LevelSelectState
                self.game.change_state(LevelSelectState(self.game))

    def update(self, dt):
        pass

    def draw(self):
        self.game.screen.fill((20, 20, 20))  # fondo provisional
        self.level.draw(self.game.screen)
