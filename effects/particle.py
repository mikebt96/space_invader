# effects/particle.py
import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(
            random.uniform(-200, 200),
            random.uniform(-200, 200)
        )
        self.life = 1.0

    def update(self, dt):
        self.life -= dt
        self.pos += self.vel * dt
        self.vel *= 0.92

    def draw(self, win):
        if self.life > 0:
            pygame.draw.circle(
                win,
                (255, 180, 0),
                (int(self.pos.x), int(self.pos.y)),
                2
            )
