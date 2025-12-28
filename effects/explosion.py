# effects/explosion.py
import pygame

class Explosion:
    def __init__(self, x, y, frames):
        self.frames = frames
        self.index = 0
        self.timer = 0
        self.frame_rate = 0.04
        self.x = x
        self.y = y
        self.done = False

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_rate:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.done = True

    def draw(self, win):
        if not self.done:
            frame = self.frames[self.index]
            rect = frame.get_rect(center=(self.x, self.y))
            win.blit(frame, rect)
