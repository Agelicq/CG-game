
"""Módulo de Enemigos del Juego.

Este módulo contiene la clase Enemy que representa
enemigos con patrullaje basico en el mapa.
"""

import os
import pygame

# Constantes de configuración del enemigo
ENEMY_SPEED = 2
SPRITE_SIZE = (65, 65)


class Enemy(pygame.sprite.Sprite):
    """Clase que representa un enemigo en el juego.
    
    Los enemigos patrullan una distancia determinada y pueden
    dañar al jugador por contacto. Tienen animaciones de caminar
    y sistema de vida.
    
    Atributos:
        pos (pygame.Vector2): Posición actual del enemigo.
        vel (pygame.Vector2): Velocidad de movimiento.
        health (int): Puntos de vida del enemigo.
        anim_walk (list): Lista de frames de animación de caminar.
        frame (float): Frame actual de la animación.
        frame_speed (float): Velocidad de reproducción de animación.
        facing_right (bool): Dirección hacia la que mira el enemigo.
    """
    
    def __init__(self, x, y, patrol_dist):
        """Inicializa un nuevo enemigo.
        
        Args:
            x (int): Coordenada X inicial del enemigo.
            y (int): Coordenada Y inicial del enemigo.
            patrol_dist (int): Distancia de patrullaje en píxeles.
        """
        super().__init__()

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(ENEMY_SPEED, 0)
        self.health = 5  # Puntos de vida iniciales

        # Cargar animaciones de caminar desde assets
        self.anim_walk = []
        folder = "assets/images/enemy"
        for filename in sorted(os.listdir(folder)):
            if filename.startswith("WALK"):
                img = pygame.image.load(f"{folder}/{filename}").convert_alpha()
                img = pygame.transform.scale(img, SPRITE_SIZE)
                self.anim_walk.append(img)

        # Configuración de animación
        self.frame = 0
        self.frame_speed = 0.1

        # Configuración visual inicial
        self.image = self.anim_walk[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing_right = True

        # Patrulla
        self.start_x = x
        self.patrol_dist = patrol_dist

        # Estado
        self.alive = True

    def update_ai(self):
        # Cambiar dirección si alcanza límites de patrulla
        if self.pos.x > self.start_x + self.patrol_dist:
            self.vel.x = -ENEMY_SPEED
            self.facing_right = False
        elif self.pos.x < self.start_x - self.patrol_dist:
            self.vel.x = ENEMY_SPEED
            self.facing_right = True

    def update_animation(self):
        self.frame = (self.frame + self.frame_speed) % len(self.anim_walk)
        img = self.anim_walk[int(self.frame)]

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False
        self.kill()
        self.death_sound = pygame.mixer.Sound("assets/music/enemydie.wav")
        self.death_sound.set_volume(0.4)
        self.death_sound.play()
        print("Enemy destroyed!")



    def update(self, dt):
        if not self.alive:
            return

        self.update_ai()

        # Movimiento
        self.pos.x += self.vel.x
        self.rect.x = int(self.pos.x)

        self.update_animation()
