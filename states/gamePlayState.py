import pygame
import sys
from core.state import State
from level.level import Level
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.stalactite import Stalactite
from states.gameOverState import GameOverState
from sprites.collectible import Collectible

class GameplayState(State):
    def __init__(self, game, planet_name):
        super().__init__(game)
        self.level = Level(planet_name)
        self.player = Player(self, self.level.player_spawn)
        
        # 1. Cargamos la imagen desde el archivo
        bg_image = pygame.image.load("assets/images/bgGlacius.png").convert() 
        self.background = pygame.transform.scale(bg_image, self.game.screen.get_size())


        x = 500
        y = 150
        #posisicion inicial para stalacdita luego se pondra en el mapa
        self.enemies = pygame.sprite.Group()
        #posicion de enemigos temporal 
        self.enemies.add(Enemy((550, 180)))
        self.bullets = pygame.sprite.Group()
        self.stalactites = pygame.sprite.Group()
        self.stalactites.add(Stalactite(x, y))
        self.collectibles = pygame.sprite.Group()

        fragment_img = pygame.image.load("assets/images/alfa.png").convert_alpha()
        fragment_img = pygame.transform.scale(fragment_img, (60, 55))
        heal_img = pygame.image.load("assets/images/item.png").convert_alpha()
        heal_img = pygame.transform.scale(heal_img, (55, 55))

        self.collectibles.add(Collectible(80, 170, fragment_img, type="fragment"))
        self.collectibles.add(Collectible(100, 300, heal_img, type="heal"))




    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from states.level_select import LevelSelectState
                self.game.change_state(LevelSelectState(self.game))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                import states.menu as menu
                self.game.change_state(menu.MenuState(self.game))


    def update(self, dt):
        self.player.update(dt, self.level.tiles)
        self.enemies.update(dt)
        self.bullets.update(self.level.tiles)
        self.stalactites.update(self.player, self.level.tiles)

        # Enemigo colisiona con Player -> daño
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.player.take_damage(10)

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage()
                    bullet.kill()
            
        if not self.player.alive:
            self.game.change_state(GameOverState(self.game))
            return
        
        hits = pygame.sprite.spritecollide(self.player, self.collectibles, dokill=True)
        for item in hits:
            if item.type == "fragment":
                self.player.collected_fragment = True
                print("Fragment collected!")
            elif item.type == "heal":
                self.player.health = min(50, self.player.health + 10)
                print("Health")


    def draw_health_bar(self):
        max_width = 200
        height = 18
        x, y = 20, 20

        health_ratio = max(self.player.health, 0) / 50 #vida maxima  
        current_width = int(max_width * health_ratio)

        # Borde
        pygame.draw.rect(self.game.screen, (255,255,255), (x, y, max_width, height), 2)

        # Barra interior
        if health_ratio > 0.6:
            color = (0, 255, 0)  # verde
        elif health_ratio > 0.3:
            color = (255, 255, 0)  # amarillo
        else:
            color = (255, 0, 0)  # rojo

        pygame.draw.rect(self.game.screen, color, (x + 2, y + 2, current_width - 4, height - 4))


    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        #self.game.screen.fill((10, 10, 15))
        self.level.draw(self.game.screen)
        self.game.screen.blit(self.player.image, self.player.rect)
        self.bullets.draw(self.game.screen)
        self.enemies.draw(self.game.screen)
        self.draw_health_bar()
        self.stalactites.draw(self.game.screen)
        self.collectibles.draw(self.game.screen)


