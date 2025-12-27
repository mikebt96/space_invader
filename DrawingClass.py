import pygame
import os
from EnemyClass import Enemy
from ShipClass import Ship
from GameClass import Game
from BulletClass import Bullet
import sys

# Obtener la ruta del directorio del script y construir la ruta al fondo
base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
BACKGROUND = pygame.image.load(os.path.join(base_path, 'img', 'background.png'))

WIDTH, HEIGTH = 800, 600

class Drawing:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont('comicsans', 50)
      
    def drawing(self, game, player, enemies, FPS, puntos):
        self.window.blit(BACKGROUND, (0, 0))
        player.fire(self.window)

        for enemy in enemies[:]:
            enemy.draw(self.window)
        
        player.draw(self.window)

        game.draw_HUD()
        
        points_label = self.font.render(f'Points: {puntos}', 1, (255, 255, 255))
        self.window.blit(points_label, (HEIGTH / 2, 10))
        
        pygame.display.update()
