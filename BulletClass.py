import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -600 # Velocidad negativa para ir hacia arriba

    def update(self, dt):
        # Movimiento independiente de los FPS
        self.rect.y += self.speed * dt
        
        # Eliminar del juego si sale de la pantalla para no consumir RAM
        if self.rect.bottom < 0:
            self.kill()