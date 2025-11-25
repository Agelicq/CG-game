import pygame

PROJECTILE_SPEED = 12
PROJECTILE_SIZE = (20, 6)   # Ajustable según arte

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface(PROJECTILE_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, *PROJECTILE_SIZE)) 
        self.rect = self.image.get_rect(midleft=(x, y)) if direction > 0 else self.image.get_rect(midright=(x, y))

        self.direction = direction
        self.speed = PROJECTILE_SPEED
        self.alive = True

    def update(self, tiles):
        self.rect.x += self.direction * self.speed

        # eliminar proyectil si toca un tile
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.kill()
                return

        # eliminar si sale de pantalla
        if self.rect.right < 0 or self.rect.left > 800:  # Ajustar a WIDTH si usas constante
            self.kill()
