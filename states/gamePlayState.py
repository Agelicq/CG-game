import pygame
import sys
from core.state import State
from level.level import Level
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.stalactite import Stalactite
from states.gameOverState import GameOverState
from sprites.collectible import Collectible
from states.timer import GameTimer
import time

class GameplayState(State):
    def __init__(self, game, planet_name, player_data):
        super().__init__(game)
        self.player_data = player_data  # Guardamos la mochila
        self.planet_name = planet_name
        self.level = Level(planet_name)
        self.start_time = time.time() 
        self.timer = GameTimer()
        
        self.player = Player(self, self.level.player_spawn)

        
        
        # Background proveniente del nivel
        self.background = self.level.background

        # Grupos generados por el nivel
        self.enemies = self.level.enemies
        self.stalactites = self.level.stalactites
        self.collectibles = self.level.collectibles
        self.bullets = pygame.sprite.Group()   # solo se usa para balas

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from states.level_select import LevelSelectState
                # AGREGA self.player_data AQUÍ TAMBIÉN:
                self.game.change_state(LevelSelectState(self.game, self.player_data))

    def update(self, dt):
        self.player.update(dt, self.level.tiles)
        self.enemies.update(dt)
        self.bullets.update(self.level.tiles)
        self.stalactites.update(self.player, self.level.tiles)

        # Enemigo golpea al jugador
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.player.take_damage(10)

        # Bala golpea enemigo
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage()
                    bullet.kill()

        # Jugador muerto
        if not self.player.alive:
            self.game.change_state(GameOverState(self.game))
            return


        # Recolección
        hits = pygame.sprite.spritecollide(self.player, self.level.collectibles, dokill=True)
        for item in hits:
            if item.type == "fragment":
                # 1. CALCULAR TIEMPO DEL NIVEL
                end_time = time.time()
                level_duration = end_time - self.start_time
                
                # 2. ACTUALIZAR LA MOCHILA (ACUMULAR)
                self.player_data["total_time"] += level_duration
                self.player_data["levels_done"].append(self.planet_name)
                
                print(f"Nivel terminado en: {round(level_duration, 2)}s")
                print(f"Tiempo Total Acumulado: {round(self.player_data['total_time'], 2)}s")

                # 3. VOLVER AL SELECTOR CON LOS DATOS ACTUALIZADOS
                from states.level_select import LevelSelectState
                self.game.change_state(LevelSelectState(self.game, self.player_data))

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
        scaled_bg = pygame.transform.scale(self.background, self.game.screen.get_size())
        self.game.screen.blit(scaled_bg, (0, 0))
        self.level.draw(self.game.screen)

        self.collectibles.draw(self.game.screen)
        self.enemies.draw(self.game.screen)
        self.stalactites.draw(self.game.screen)
        self.bullets.draw(self.game.screen)


        self.game.screen.blit(self.player.image, self.player.rect)

        self.draw_health_bar()
        self.timer.draw(self.game.screen, self.start_time)

