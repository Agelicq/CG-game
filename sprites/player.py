import pygame
import os
from sprites.projectile import Projectile
import pygame.mixer

GRAVITY = 0.55
JUMP_SPEED = -12
MOVE_SPEED = 4
SPRITE_SIZE = (60, 60)

class Player(pygame.sprite.Sprite):
    def __init__(self, game, spawn_pos):
        super().__init__()

        self.game = game
        self.pos = pygame.Vector2(spawn_pos)
        self.vel = pygame.Vector2(0, 0)
        self.shoot_cooldown = 0
        self.shoot_delay = 250  # milisegundos entre disparos
        self.can_shoot = True  
        self.shoot_timer = 0      
        self.shooting = False
        self.shoot_anim_timer = 0 

        self.shoot_sound = pygame.mixer.Sound("assets/music/laserpew.wav")
        self.shoot_sound.set_volume(0.4)

        #vida maxima del player
        self.health = 50
        self.invincible = False
        self.invincible_timer = 0

        self.collected_fragment = False
        self.damage_timer = 0
        self.pain = False

        self.animations = {
            "idle": [], 
            "run": [], 
            "jump": [],
            "shot": [],
            "damage": [],
            "collect": []}
        
        self.load_animations()

        self.state = "idle"
        self._prev_state = None
        self.frame = 0
        self.frame_speed = 0.08

        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))

        self.facing_right = True
        self.on_ground = False


    def load_animations(self):
        folder = "assets/images/player"

        # Orden fijo para evitar mezcla visual
        idle_files  = ["IDLE1.png", "IDLE2.png"]
        run_files   = ["RUN1.png", "RUN2.png"]
        jump_files  = ["JUMP1.png", "JUMP2.png", "JUMP3.png"]
        shot_files  = ["SHOT1.png"]
        damage_files = ["DAMAGE1.png"]

        for name in idle_files:
            img = pygame.image.load(f"{folder}/{name}").convert_alpha()
            img = pygame.transform.scale(img, SPRITE_SIZE)
            self.animations["idle"].append(img)

        for name in run_files:
            img = pygame.image.load(f"{folder}/{name}").convert_alpha()
            img = pygame.transform.scale(img, SPRITE_SIZE)
            self.animations["run"].append(img)

        for name in jump_files:
            img = pygame.image.load(f"{folder}/{name}").convert_alpha()
            img = pygame.transform.scale(img, SPRITE_SIZE)
            self.animations["jump"].append(img)

        for name in shot_files:
            img = pygame.image.load(f"{folder}/{name}").convert_alpha()
            img = pygame.transform.scale(img, SPRITE_SIZE)
            self.animations["shot"].append(img)

        for name in damage_files:
            img = pygame.image.load(f"{folder}/{name}").convert_alpha()
            img = pygame.transform.scale(img, SPRITE_SIZE)
            self.animations["damage"].append(img)


    def input(self):
        keys = pygame.key.get_pressed()

        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -MOVE_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel.x = MOVE_SPEED
            self.facing_right = True
        if keys[pygame.K_UP] and self.on_ground:
            self.vel.y = JUMP_SPEED
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
    # posición del proyectil en la mano / frente del astro-bot
        x = self.rect.centerx + (25 if self.facing_right else -25)
        y = self.rect.centery - 5

        proj = Projectile(x, y, 1 if self.facing_right else -1)
        self.projectiles.add(proj)
        self.shoot_sound.play()


    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > 10:
            self.vel.y = 10

    def move_and_collide(self, tiles):
        # Movimiento horizontal
        self.pos.x += self.vel.x
        self.rect.x = int(self.pos.x)
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:
                    self.rect.right = tile.rect.left
                elif self.vel.x < 0:
                    self.rect.left = tile.rect.right
                self.pos.x = self.rect.x
                
        if self.rect.left < 0:  # Si se sale por la izquierda
            self.rect.left = 0
            self.pos.x = self.rect.x
            self.vel.x = 0  # Detener movimiento horizontal

        # Movimiento vertical
        self.pos.y += self.vel.y
        self.rect.y = int(self.pos.y)
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0
                self.pos.y = self.rect.y

        # aplicar fricción según el tile donde se está parado
        for tile in tiles:
            if self.rect.colliderect(tile.rect) and self.on_ground:
                if tile.type == "ice":
                    self.vel.x *= 0.97    # frena muy poco = hielo
                else:
                    self.vel.x *= 0.75    # frena rápido = suelo normal
                break



    def update_animation(self):
        # 1) Determinar estado ---- (una sola vez)
        if not self.on_ground and self.vel.y < 0:
            new_state = "jump"
        elif not self.on_ground and self.vel.y > 0:
            new_state = "idle"
        elif abs(self.vel.x) > 0.2:
            new_state = "run"
        elif self.shooting:
            new_state = "shot"
        elif self.pain:
            new_state = "damage"
        else:
            new_state = "idle"

        # 2) Si el estado cambió, reiniciar frame
        if new_state != self.state:
            self.state = new_state
            self.frame = 0

        # 3) Elegir velocidad de animación por estado
        if self.state == "idle":
            self.frame_speed = 0.04         # lento porque son 2 frames
        elif self.state == "run":
            self.frame_speed = 0.15         # rápido para sentirse fluido
        elif self.state == "jump":
            self.frame_speed = 0.10
        elif self.state == "shot":
            self.frame_speed = 0.04
        elif self.state == "damage":
            self.frame_speed = 0.01


        # 4) Actualizar frame solo si el estado tiene múltiples imágenes
        frames = self.animations[self.state]

        if self.state == "idle":
            image = frames[0]   # idle = frame fijo
        else:
            self.frame = (self.frame + self.frame_speed) % len(frames)
            image = frames[int(self.frame)]

        # 5) Flip horizontal
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        # 6) Mantener siempre la posición de los pies
        old_midbottom = self.rect.midbottom
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_timer = 0.5
            self.state = "damage"
            self.frame = 0
            self.pain = True
            self.damage_timer = 0.1   # duración de la animación
            print(f"Player damage! Health = {self.health}")

    def die(self):
        print("PLAYER DEAD")
        self.alive = False
        self.health = 0



    def update(self, dt, tiles):
        self.input()
        self.apply_gravity()
        self.move_and_collide(tiles)
        self.update_animation()
        self.game.bullets.update(tiles)

        if self.damage_timer > 0:
            self.damage_timer -= dt
            if self.damage_timer <= 0:
                self.state = "idle"

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1000 * dt

        if not self.can_shoot:
            self.shoot_timer -= dt
            if self.shoot_timer <= 0:
                self.can_shoot = True

        if self.shooting:
            self.shoot_anim_timer -= dt
            if self.shoot_anim_timer <= 0:
                self.shooting = False
        
        if self.health <= 0:
            self.die()

        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
                self.pain = False

        if self.rect.top > 800:  # valor grande para que realmente haya vacío
            self.die()





