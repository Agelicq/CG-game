#!/usr/bin/env python3
"""Módulo del Jugador Principal.

Este módulo contiene la clase Player que representa al personaje
controlable por el jugador en Astro Lost. Incluye mecánicas de
movimiento, salto, disparo, escalada y sistema de vida.
"""

import os
import pygame
import pygame.mixer

from sprites.projectile import Projectile

# Constantes de física y configuración del jugador
GRAVITY = 0.55        # Fuerza de gravedad aplicada por frame
JUMP_SPEED = -12      # Velocidad inicial del salto (negativa = hacia arriba)
MOVE_SPEED = 4        # Velocidad base de movimiento horizontal
SPRITE_SIZE = (60, 60) # Tamaño de los sprites del jugador


class Player(pygame.sprite.Sprite):
    """Clase que representa al jugador controlable.
    
    El jugador es el personaje principal que puede moverse, saltar,
    disparar, trepar paredes y interactuar con el entorno. Tiene
    sistema de vida, invencibilidad temporal y múltiples animaciones.
    
    Atributos:
        game: Referencia al objeto GameManager principal.
        pos (pygame.Vector2): Posición actual del jugador.
        vel (pygame.Vector2): Velocidad de movimiento actual.
        health (int): Puntos de vida actuales (máximo 80).
        facing_right (bool): Dirección hacia la que mira el jugador.
        on_ground (bool): Si el jugador está tocando el suelo.
        on_ice (bool): Si el jugador está sobre hielo.
        shooting (bool): Si está en animación de disparo.
        invincible (bool): Si tiene invencibilidad temporal.
        animations (dict): Diccionario con todas las animaciones.
    """
    
    def __init__(self, game, spawn_pos):
        """Inicializa un nuevo jugador.
        
        Args:
            game: Instancia del GameManager principal.
            spawn_pos (tuple): Coordenadas (x, y) de aparición inicial.
        """
        super().__init__()

        # Referencias y posicionamiento
        self.game = game
        self.pos = pygame.Vector2(spawn_pos)
        self.vel = pygame.Vector2(0, 0)
        
        # Sistema de disparo
        self.shoot_cooldown = 0
        self.shoot_delay = 250  # Milisegundos entre disparos
        self.can_shoot = True
        self.shoot_timer = 0
        self.shooting = False
        self.shoot_anim_timer = 0
        self.poison_wall_timer = 0

        # Efectos de sonido
        self.shoot_sound = pygame.mixer.Sound("assets/music/laserpew.wav")
        self.shoot_sound.set_volume(0.4)

        # Sistema de vida y daño
        self.health = 80  # Vida máxima del jugador
        self.invincible = False
        self.invincible_timer = 0

        # Estados especiales
        self.collected_fragment = False
        self.damage_timer = 0
        self.pain = False

        # Sistema de animaciones
        self.animations = {
            "idle": [],     # Animación de reposo
            "run": [],      # Animación de correr
            "jump": [],     # Animación de salto
            "shot": [],     # Animación de disparo
            "damage": [],   # Animación de daño
            "collect": []   # Animación de recoger objetos
        }
        
        self.load_animations()

        # Control de animaciones
        self.state = "idle"
        self._prev_state = None
        self.frame = 0
        self.frame_speed = 0.08

        # Configuración visual inicial
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))

        # Estados de movimiento
        self.facing_right = True
        self.on_ground = False
        self.on_ice = False  # Estado sobre hielo

    def load_animations(self):
        """Carga todas las animaciones del jugador desde archivos.
        
        Lee los sprites desde la carpeta assets/images/player y los
        organiza por tipo de animación. Escala todas las imágenes
        al tamaño estándar definido por SPRITE_SIZE.
        """
        folder = "assets/images/player"

        # Definir archivos de animación en orden específico
        animation_files = {
            "idle": ["IDLE1.png", "IDLE2.png"],
            "run": ["RUN1.png", "RUN2.png"],
            "jump": ["JUMP1.png", "JUMP2.png", "JUMP3.png"],
            "shot": ["SHOT1.png"]
        }

        # Cargar cada animación
        for anim_name, file_list in animation_files.items():
            for filename in file_list:
                try:
                    img = pygame.image.load(f"{folder}/{filename}").convert_alpha()
                    img = pygame.transform.scale(img, SPRITE_SIZE)
                    self.animations[anim_name].append(img)
                except pygame.error as e:
                    print(f"Error cargando {filename}: {e}")



    def input(self):
        """Procesa la entrada del teclado del jugador.
        
        Maneja el movimiento horizontal, salto y disparo basado en
        las teclas presionadas. Ajusta la velocidad según el tipo
        de superficie (hielo = más rápido).
        
        Controles:
            - Flechas izq/der: Movimiento horizontal
            - Flecha arriba: Salto (solo en el suelo)
            - Espacio: Disparo (con cooldown)
        """
        keys = pygame.key.get_pressed()

        # Calcular velocidad actual (doble en hielo)
        current_speed = MOVE_SPEED * 2 if hasattr(self, 'on_ice') and self.on_ice else MOVE_SPEED
        
        # Movimiento horizontal
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -current_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel.x = current_speed
            self.facing_right = True
            
        # Salto (solo si está en el suelo)
        if keys[pygame.K_UP] and self.on_ground:
            self.vel.y = JUMP_SPEED
            
        # Disparo (con sistema de cooldown)
        if keys[pygame.K_SPACE] and self.can_shoot:
            direction = 1 if self.facing_right else -1
            bullet = Projectile(self.rect.centerx, self.rect.centery, direction)
            self.game.bullets.add(bullet)
            self.can_shoot = False
            self.shoot_timer = 0.25
            self.shooting = True
            self.shoot_anim_timer = 0.18
            self.shoot_sound.play()


    def shoot(self):
        """Método auxiliar de disparo (actualmente no utilizado).
        
        Crea un proyectil en la posición de la mano del jugador.
        El disparo principal se maneja en el método input().
        """
        # Calcular posición del proyectil frente al jugador
        x = self.rect.centerx + (25 if self.facing_right else -25)
        y = self.rect.centery - 5

        proj = Projectile(x, y, 1 if self.facing_right else -1)
        self.projectiles.add(proj)
        self.shoot_sound.play()

    def apply_gravity(self):
        """Aplica la fuerza de gravedad al jugador.
        
        Incrementa la velocidad vertical hacia abajo cada frame,
        con un límite máximo de velocidad de caída.
        """
        self.vel.y += GRAVITY
        if self.vel.y > 10:
            self.vel.y = 10  # Velocidad máxima de caída

    def move_and_collide(self, tiles):
        """Maneja el movimiento del jugador y las colisiones con tiles.
        
        Procesa el movimiento horizontal y vertical por separado,
        resolviendo colisiones con tiles. Incluye sistema de fricción
        y límites de pantalla.
        
        Args:
            tiles: Grupo de tiles para verificar colisiones.
        """
        # === MOVIMIENTO HORIZONTAL ===
        self.pos.x += self.vel.x
        self.rect.x = int(self.pos.x)
        
        # Resolver colisiones horizontales
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:  # Moviendose a la derecha
                    self.rect.right = tile.rect.left
                elif self.vel.x < 0:  # Moviendose a la izquierda
                    self.rect.left = tile.rect.right
                self.pos.x = self.rect.x
                
        # Límite izquierdo de pantalla
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x
            self.vel.x = 0

        # === MOVIMIENTO VERTICAL ===
        self.pos.y += self.vel.y
        self.rect.y = int(self.pos.y)
        self.on_ground = False
        
        # Resolver colisiones verticales
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:  # Cayendo
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:  # Subiendo
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0
                self.pos.y = self.rect.y

        # === SISTEMA DE FRICCIÓN ===
        for tile in tiles:
            if self.rect.colliderect(tile.rect) and self.on_ground:
                if tile.type == "ice":
                    self.vel.x *= 0.98    # Hielo: muy resbaloso
                else:
                    self.vel.x *= 0.75    # Suelo normal: fricción estándar
                break

        # === SISTEMA DE ESCALADA EN PAREDES ===
        keys = pygame.key.get_pressed()
        climb_speed = 3  # Velocidad de escalada en píxeles por frame

        # Detectar contacto lateral con paredes escalables
        touching_left = False
        touching_right = False

        # Áreas de detección lateral (pequeñas cajas en los lados)
        left_check = pygame.Rect(self.rect.left - 2, self.rect.top + 4, 2, self.rect.height - 8)
        right_check = pygame.Rect(self.rect.right, self.rect.top + 4, 2, self.rect.height - 8)

        for tile in tiles:
            if tile.type == "climb":
                # Pared escalable normal
                if left_check.colliderect(tile.rect):
                    touching_left = True
                if right_check.colliderect(tile.rect):
                    touching_right = True
            elif tile.type == "poisonWall":
                # Pared venenosa escalable (con daño)
                if left_check.colliderect(tile.rect) or right_check.colliderect(tile.rect):
                    self.poison_wall = True
                    # Aplicar daño con cooldown
                    if self.poison_wall_timer <= 0:
                        self.take_damage(4)
                        self.poison_wall_timer = 0.6  # Cooldown antes del siguiente daño

        # Determinar si el jugador quiere trepar
        wants_to_climb = False
        climb_dir = 0
        
        if touching_left and (keys[pygame.K_LEFT] or keys[pygame.K_UP]):
            wants_to_climb = True
            climb_dir = -1  # Pared a la izquierda
        elif touching_right and (keys[pygame.K_RIGHT] or keys[pygame.K_UP]):
            wants_to_climb = True
            climb_dir = 1   # Pared a la derecha

        # Ejecutar mecánica de escalada
        if wants_to_climb and not self.on_ground:
            # Anular gravedad durante la escalada
            self.vel.y = 0

            # Controles verticales de escalada
            if keys[pygame.K_UP]:
                self.pos.y -= climb_speed  # Subir
            elif keys[pygame.K_DOWN]:
                self.pos.y += climb_speed  # Bajar

            # Prevenir movimiento horizontal durante escalada
            self.vel.x = 0

            # Sincronizar posición
            self.rect.y = int(self.pos.y)
            self.rect.x = int(self.pos.x)



    def update_animation(self):
        """Sistema de animación avanzado del jugador.
        
        Determina el estado de animación basado en múltiples factores
        (movimiento, salto, disparo) y actualiza frames con velocidades
        específicas por estado. Incluye flip horizontal y anclaje de posición.
        """
        # === DETERMINACIÓN DE ESTADO DE ANIMACIÓN ===
        if not self.on_ground and self.vel.y < 0:
            new_state = "jump"      # Saltando (subiendo)
        elif not self.on_ground and self.vel.y > 0:
            new_state = "idle"      # Cayendo (usar idle)
        elif abs(self.vel.x) > 0.2:
            new_state = "run"       # Corriendo
        elif self.shooting:
            new_state = "shot"      # Disparando
        else:
            new_state = "idle"      # Quieto

        # === REINICIO DE ANIMACIÓN AL CAMBIAR ESTADO ===
        if new_state != self.state:
            self.state = new_state
            self.frame = 0

        # === CONFIGURACIÓN DE VELOCIDADES POR ESTADO ===
        if self.state == "idle":
            self.frame_speed = 0.04     # Lento (pocos frames)
        elif self.state == "run":
            self.frame_speed = 0.15     # Rápido (sensación fluida)
        elif self.state == "jump":
            self.frame_speed = 0.10     # Moderado
        elif self.state == "shot":
            self.frame_speed = 0.04     # Lento (precisión visual)

        # === ACTUALIZACIÓN DE FRAMES ===
        frames = self.animations[self.state]

        if self.state == "idle":
            image = frames[0]   # Idle usa frame fijo
        else:
            # Animación cíclica para otros estados
            self.frame = (self.frame + self.frame_speed) % len(frames)
            image = frames[int(self.frame)]

        # === FLIP HORIZONTAL SEGÚN DIRECCIÓN ===
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        # === ANCLAJE DE POSICIÓN (mantener pies en lugar) ===
        old_midbottom = self.rect.midbottom
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

    def take_damage(self, amount):
        """Aplica daño al jugador.
        
        Reduce la vida del jugador y activa el estado de invencibilidad
        temporal para evitar daño continuo.
        
        Args:
            amount (int): Cantidad de daño a aplicar.
        """
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_timer = 0.5  # Medio segundo de invencibilidad
            self.state = "damage"
            self.frame = 0
            self.pain = True
            print(f"Player damage! Health = {self.health}")

    def die(self):
        """Maneja la muerte del jugador.
        
        Establece el estado de muerte y resetea la vida a 0.
        """
        print("PLAYER DEAD")
        self.alive = False
        self.health = 0


    def update(self, dt, tiles):
        """Método principal de actualización del jugador.
        
        Coordina todos los sistemas del jugador en orden específico:
        entrada, física, colisiones, animaciones, proyectiles, timers,
        estados especiales y detección de peligros ambientales.
        
        Args:
            dt (float): Delta time para cálculos temporales.
            tiles: Lista de tiles para colisiones y efectos.
        """
        # === SISTEMAS PRINCIPALES ===
        self.input()                    # Procesar entrada del usuario
        self.apply_gravity()            # Aplicar gravedad
        self.move_and_collide(tiles)    # Movimiento y colisiones
        self.update_animation()         # Sistema de animación
        self.game.bullets.update(tiles) # Actualizar proyectiles
        
        # === SISTEMA DE TIMERS ===
        # Timer de daño (recuperación visual)
        if self.damage_timer > 0:
            self.damage_timer -= dt
            if self.damage_timer <= 0:
                self.state = "idle"

        # Cooldown de disparo
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1000 * dt

        # Timer de capacidad de disparo
        if not self.can_shoot:
            self.shoot_timer -= dt
            if self.shoot_timer <= 0:
                self.can_shoot = True

        # Timer de animación de disparo
        if self.shooting:
            self.shoot_anim_timer -= dt
            if self.shoot_anim_timer <= 0:
                self.shooting = False
        
        # === SISTEMA DE VIDA Y MUERTE ===
        if self.health <= 0:
            self.die()

        # Sistema de invencibilidad temporal
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
                self.pain = False

        # Muerte por caída al vacío
        if self.rect.top > 800:
            self.die()

        # === SISTEMA DE PELIGROS AMBIENTALES ===
        self.on_danger = False
        if self.on_ground:
            # Área de detección en los pies del jugador
            foot_rect = pygame.Rect(self.rect.x, self.rect.bottom + 1, self.rect.width, 2)

            for tile in tiles:
                if (tile.type == "ice" or tile.type == "lava") and foot_rect.colliderect(tile.rect):
                    self.on_danger = True
                    break
                elif tile.type == "poison" and foot_rect.colliderect(tile.rect):
                    self.take_damage(5)  # Daño directo por veneno
                    break

        # Aplicar daño continuo por superficies peligrosas
        if self.on_danger:
            self.take_damage(1)

        # === COOLDOWN DE PARED VENENOSA ===
        if self.poison_wall_timer > 0:
            self.poison_wall_timer -= dt





