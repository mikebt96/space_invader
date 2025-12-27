import pygame
import random
import os
from ShipClass import Ship
import sys

# Obtener la ruta del directorio del script y construir las rutas a las imágenes
base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

BULLET_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'bullet_image.png'))
ENEMY_BLUE_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'enemy_blue_image.png'))
ENEMY_GREEN_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'enemy_green_image.png'))
ENEMY_PURPLE_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'enemy_purple_image.png'))
SHOT_BLUE_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'shot_blue.png'))
SHOT_GREEN_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'shot_green.png'))
SHOT_PURPLE_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'shot_purple.png'))

class Enemy(Ship):
    COLOR = {'blue': (ENEMY_BLUE_IMAGE, SHOT_BLUE_IMAGE),
             'green': (ENEMY_GREEN_IMAGE, SHOT_GREEN_IMAGE),
             'purple': (ENEMY_PURPLE_IMAGE, SHOT_PURPLE_IMAGE)}
    
    def __init__(self, speed = 0, x = 50, y = 50, color = 'blue', health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.bullet_img = self.COLOR["blue"]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.speed = speed

    def move(self):
        self.y = self.y + 1
        
    def create(self, amount):
        enemies = []
        for i in range(amount):
            x = random.randrange(20, WIDTH - ENEMY_BLUE_IMAGE.get_width() - 20)
            y = random.randrange(-1000, -100)
            color = random.choice(["blue", "green", "purple"])
            speed = self.speed
            enemy = Enemy(x=x, y=y, color=color, speed=speed)
            enemies.append(enemy)
        return enemies

    def increase_speed(self):
        self.speed *= 1.02

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

########Código de ejemplo

def main():
    run = True
    clock = pygame.time.Clock()
    enemies = Enemy(1)
    enemies = enemies.create(5)
    
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for enemy in enemies:
            enemy.move()
        WIN.fill((0, 0, 0))
        
        for enemy in enemies:
            enemy.draw(WIN)
            
        pygame.display.update()
    pygame.quit()

# main()
