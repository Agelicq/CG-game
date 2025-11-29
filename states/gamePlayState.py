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

        
        # enemigos
        self.enemies = pygame.sprite.Group()
        for x, y in self.level.enemy_spawns:
            self.enemies.add(Enemy(x, y + 18, 120))
        self.bullets = pygame.sprite.Group()


        # Cargar imagen de stalactita
        stalactite_img = pygame.image.load("assets/images/stalactite.png").convert_alpha()
        stalactite_img = pygame.transform.scale(stalactite_img, (16, 32))

        #stalactitas
        self.stalactites = pygame.sprite.Group()
        for x, y in self.level.stalactite_spawns:
            self.stalactites.add(Stalactite(x, y, stalactite_img))


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

        # Enemigo colisiona con Player = daño
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
        
        hits = pygame.sprite.spritecollide(self.player, self.level.collectibles, dokill=True)
        for item in hits:
            if item.type == "fragment":
                self.player.collected_fragment = True
                print("Fragment collected!")
            elif item.type == "heal":
                self.health_sound = pygame.mixer.Sound("assets/music/health.wav")
                self.health_sound.set_volume(0.4)
                self.health_sound.play()
                self.player.health = min(50, self.player.health + 20) #cuanto cura al player
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
            color = (126, 252, 126)  # verde
        elif health_ratio > 0.3:
            color = (181, 66, 0)  # amarillo
        else:
            color = (181, 33, 0)  # rojo

        pygame.draw.rect(self.game.screen, color, (x + 2, y + 2, current_width - 4, height - 4))


    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        self.level.draw(self.game.screen)
        self.game.screen.blit(self.player.image, self.player.rect)
        self.bullets.draw(self.game.screen)
        self.enemies.draw(self.game.screen)
        self.draw_health_bar()
        self.stalactites.draw(self.game.screen)
        self.level.collectibles.draw(self.game.screen)


