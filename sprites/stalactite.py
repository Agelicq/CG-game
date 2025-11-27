import pygame

GRAVITY = 0.6

class Stalactite(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.start_x = x
        self.start_y = y
        self.image = image  # Usar la imagen pasada desde gamePlayState
        self.rect = self.image.get_rect(topleft=(x, y))
        self.falling = False
        self.fall_speed = 3

    def update(self, player, tiles):
        # activar si el jugador está debajo
        self.falling = True

        # Si está cayendo
        if self.falling:
            self.rect.y += self.fall_speed

            # Si toca suelo / reiniciar para caer otra vez
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    self.reset()
                    break

            # Si sale de pantalla por abajo / reiniciar también
            if self.rect.top > 600:  # alto de pantalla
                self.reset()

            # colisión con el jugador
            if self.rect.colliderect(player.rect):
                player.take_damage(15)
                self.reset()
                return

            # colisión con tiles
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    self.kill()
                    return


    def reset(self):
        self.rect.topleft = (self.start_x, self.start_y)
        self.falling = False
