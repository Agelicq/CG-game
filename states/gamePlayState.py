import pygame
import sys
from core.state import State
from level.level import Level
from sprites.player import Player
from sprites.enemy import Enemy

class GameplayState(State):
    def __init__(self, game, planet_name):
        super().__init__(game)
        self.level = Level(planet_name)
        self.player = Player(self.level.player_spawn)
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy((550, 180)))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from states.level_select import LevelSelectState
                self.game.change_state(LevelSelectState(self.game))

    def update(self, dt):
        self.player.update(dt, self.level.tiles)
        self.enemies.update(dt)

    def draw(self):
        self.game.screen.fill((10, 10, 15))
        self.level.draw(self.game.screen)
        self.game.screen.blit(self.player.image, self.player.rect)
        self.player.projectiles.draw(self.game.screen)
        self.enemies.draw(self.game.screen)
