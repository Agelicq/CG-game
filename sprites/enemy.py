import pygame
import os

ENEMY_SPEED = 2
SPRITE_SIZE = (60, 60)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_dist=120):
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(ENEMY_SPEED, 0)

        # Cargar animación WALK
        self.anim_walk = []
        folder = "assets/images/enemy"
        for filename in sorted(os.listdir(folder)):
            if filename.startswith("WALK"):
                img = pygame.image.load(f"{folder}/{filename}").convert_alpha()
                img = pygame.transform.scale(img, SPRITE_SIZE)
                self.anim_walk.append(img)

        self.frame = 0
        self.frame_speed = 0.1

        self.image = self.anim_walk[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.facing_right = True

        # Patrulla
        self.start_x = pos[0]
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

    def update(self, dt):
        if not self.alive:
            return

        self.update_ai()

        # Movimiento
        self.pos.x += self.vel.x
        self.rect.x = int(self.pos.x)

        self.update_animation()
