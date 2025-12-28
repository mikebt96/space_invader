import pygame
import random
from ShipClass import Ship

class Enemy(Ship):
    def __init__(self, x, y, color, img_dict, speed):
        super().__init__(x, y)
        self.ship_img = img_dict[color][0]
        self.bullet_img = img_dict[color][1]
        self.image = self.ship_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.y = float(y)
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.y += self.speed * dt
        self.rect.y = int(self.y)
        if self.rect.top > 800: # Fuera de pantalla
            self.kill()

    @staticmethod
    def create_wave(amount, width, img_dict, level):
        group = pygame.sprite.Group()
        for i in range(amount):
            x = random.randint(50, width - 100)
            y = random.randint(-1200, -100) # Aparecen desde arriba
            color = random.choice(['blue', 'green', 'purple'])
            speed = 100 + (level * 25)
            enemy = Enemy(x, y, color, img_dict, speed)
            group.add(enemy)
        return group