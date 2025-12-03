#!/usr/bin/env python3
"""Módulo del Estado de Juego Principal.

Este módulo contiene la clase GameplayState que maneja
la lógica principal del juego durante las partidas,
incluyendo actualización de entidades, colisiones y renderizado.
"""

# Importaciones de librerías estándar
import sys
import time

# Importaciones de terceros
import pygame

# Importaciones locales
from core.state import State
from level.level import Level
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.laser import Laser
from sprites.stalactite import Stalactite
from states.gameOverState import GameOverState
from sprites.toxic import Toxic
from sprites.collectible import Collectible
from states.timer import GameTimer


class GameplayState(State):
    """Estado principal del gameplay del juego.
    
    Maneja toda la lógica de juego durante las partidas:
    actualización de entidades, detección de colisiones,
    gestión de tiempo y transiciones de estado.
    
    Attributes:
        player_data: Datos del jugador (tiempo, progreso).
        planet_name: Nombre del planeta/nivel actual.
        level: Instancia del nivel cargado.
        player: Instancia del jugador.
        start_time: Tiempo de inicio del nivel.
        timer: Temporizador del juego.
        background: Imagen de fondo del nivel.
        enemies: Grupo de sprites de enemigos.
        stalactites: Grupo de estalactitas.
        collectibles: Grupo de objetos recolectables.
        lasers: Grupo de láseres.
        bullets: Grupo de proyectiles del jugador.
    """
    def __init__(self, game, planet_name, player_data):
        """Inicializa el estado de gameplay.
        
        Carga el nivel especificado, inicializa al jugador en su
        posición de spawn y configura todos los grupos de sprites
        y sistemas necesarios para el juego.
        
        Args:
            game: Referencia al gestor principal del juego.
            planet_name (str): Nombre del planeta/nivel a cargar.
            player_data (dict): Datos del progreso del jugador.
        """
        super().__init__(game)
        
        # === DATOS DE SESIÓN ===
        self.player_data = player_data  # Progreso del jugador
        self.planet_name = planet_name
        self.start_time = time.time()   # Inicio del nivel para timing
        self.timer = GameTimer()
        
        # === INICIALIZACIÓN DEL NIVEL ===
        self.level = Level(planet_name)
        self.background = self.level.background
        
        # === INICIALIZACIÓN DEL JUGADOR ===
        self.player = Player(self, self.level.player_spawn)
        
        # === GRUPOS DE SPRITES (desde el nivel) ===
        self.enemies = self.level.enemies
        self.stalactites = self.level.stalactites
        self.collectibles = self.level.collectibles
        self.lasers = self.level.lasers
        
        # === GRUPO DE PROYECTILES DEL JUGADOR ===
        self.bullets = pygame.sprite.Group()

    def handle_events(self):
        """Procesa los eventos de entrada durante el gameplay.
        
        Maneja la salida del juego y permite regresar al
        selector de niveles con ESC, conservando el progreso.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # === REGRESO AL SELECTOR DE NIVELES ===
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from states.level_select import LevelSelectState
                # Conservar datos del jugador al regresar
                self.game.change_state(LevelSelectState(self.game, self.player_data))

    def update(self, dt):
        """Actualiza toda la lógica del gameplay.
        
        Coordina la actualización de todas las entidades,
        procesa colisiones, maneja la recolección de objetos
        y verifica condiciones de victoria y derrota.
        
        Args:
            dt (float): Delta time para cálculos temporales.
        """
        # === ACTUALIZACIÓN DE ENTIDADES ===
        self.player.update(dt, self.level.tiles)
        self.enemies.update(dt)
        self.bullets.update(self.level.tiles)
        self.stalactites.update(self.player, self.level.tiles)
        self.lasers.update(dt, self.player)

        # === SISTEMA DE COLISIONES ===
        
        # Colisión: Enemigo daña al jugador
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.player.take_damage(10)

        # Colisión: Proyectil elimina enemigo
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage()
                    bullet.kill()

        # === VERIFICACIÓN DE ESTADO DEL JUGADOR ===
        if not self.player.alive:
            self.game.change_state(GameOverState(self.game))
            return

        # === SISTEMA DE RECOLECCIÓN ===
        hits = pygame.sprite.spritecollide(self.player, self.level.collectibles, dokill=True)
        
        for item in hits:
            if item.type == "fragment":
                # === COMPLETAR NIVEL ===
                # Calcular tiempo empleado en el nivel
                end_time = time.time()
                level_duration = end_time - self.start_time
                
                # Actualizar progreso del jugador
                self.player_data["total_time"] += level_duration
                self.player_data["levels_done"].append(self.planet_name)
                
                # Feedback al usuario
                print(f"Nivel terminado en: {round(level_duration, 2)}s")
                print(f"Tiempo Total Acumulado: {round(self.player_data['total_time'], 2)}s")

                # Regresar al selector con progreso actualizado
                from states.level_select import LevelSelectState
                self.game.change_state(LevelSelectState(self.game, self.player_data))

            elif item.type == "heal":
                # === CURACIÓN ===
                # Reproducir sonido de curación
                self.health_sound = pygame.mixer.Sound("assets/music/health.wav")
                self.health_sound.set_volume(0.4)
                self.health_sound.play()
                
                # Restaurar vida (máximo 80 HP)
                self.player.health = min(80, self.player.health + 20)
                print("Health restored")

        

    def draw_health_bar(self):
        """Dibuja la barra de vida del jugador.
        
        Renderiza una barra de vida con colores dinámicos
        que cambian según el nivel de vida actual del jugador.
        Verde (>60%), amarillo (30-60%), rojo (<30%).
        """
        # === CONFIGURACIÓN DE LA BARRA ===
        max_width = 200
        height = 18
        x, y = 20, 20

        # Calcular proporción de vida (máximo 80 HP)
        health_ratio = max(self.player.health, 0) / 80
        current_width = int(max_width * health_ratio)

        # === DIBUJAR BORDE ===
        pygame.draw.rect(self.game.screen, (255, 255, 255), (x, y, max_width, height), 2)

        # === DETERMINAR COLOR SEGÚN NIVEL DE VIDA ===
        if health_ratio > 0.6:
            color = (126, 252, 126)  # Verde: vida alta
        elif health_ratio > 0.3:
            color = (181, 66, 0)     # Amarillo: vida media
        else:
            color = (181, 33, 0)     # Rojo: vida crítica

        # === DIBUJAR BARRA INTERIOR ===
        pygame.draw.rect(self.game.screen, color, (x + 2, y + 2, current_width - 4, height - 4))

    def draw(self):
        """Renderiza todos los elementos visuales del gameplay.
        
        Dibuja el fondo, nivel, entidades y HUD en el orden
        correcto para evitar problemas de superposición.
        El orden de renderizado es crítico para la correcta
        visualización de las capas.
        """
        # === FONDO DEL NIVEL ===
        scaled_bg = pygame.transform.scale(self.background, self.game.screen.get_size())
        self.game.screen.blit(scaled_bg, (0, 0))
        
        # === ELEMENTOS DEL NIVEL ===
        self.level.draw(self.game.screen)  # Tiles y estructura
        
        # === ENTIDADES (en orden de profundidad) ===
        self.collectibles.draw(self.game.screen)   # Objetos recolectables
        self.enemies.draw(self.game.screen)        # Enemigos
        self.stalactites.draw(self.game.screen)    # Estalactitas
        self.bullets.draw(self.game.screen)        # Proyectiles
        self.level.toxic.draw(self.game.screen)    # Elementos tóxicos
        
        # Láseres (requieren renderizado especial)
        for laser in self.lasers:
            laser.draw(self.game.screen)

        # === JUGADOR (siempre visible) ===
        self.game.screen.blit(self.player.image, self.player.rect)
        
        # === INTERFAZ DE USUARIO ===
        self.draw_health_bar()  # Barra de vida
        self.timer.draw(self.game.screen, self.start_time)  # Temporizador
        


