import pygame
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img, bullet_group, bullet_img):
        super().__init__()
        self.original_image = img 
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = Vector2(x, y)
        
        # Física
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.max_speed = 450
        self.acceleration = 2200
        self.friction = 1800
        
        # Efecto Banking (Fake 3D)
        self.tilt_factor = 1.0        
        self.target_tilt = 1.0
        
        # Disparo
        self.bullet_group = bullet_group
        self.bullet_img = bullet_img 
        self.cooldown_timer = 0
        self.COOLDOWN_TIME = 250

    def input(self):
        keys = pygame.key.get_pressed()
        self.acc = Vector2(0, 0)
        self.target_tilt = 1.0 # Vuelve a la normalidad si no hay teclas

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.acc.x = -self.acceleration
            self.target_tilt = 0.6 # Se inclina
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.acc.x = self.acceleration
            self.target_tilt = 0.6
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.acc.y = -self.acceleration
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.acc.y = self.acceleration
            
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.cooldown_timer > self.COOLDOWN_TIME:
            from BulletClass import Bullet
            new_bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_img) 
            self.bullet_group.add(new_bullet)
            self.cooldown_timer = now

    def update(self, dt, width, height):
        self.input()
        
        # Aplicar Banking suave
        self.tilt_factor += (self.target_tilt - self.tilt_factor) * 0.1
        nw = int(self.original_image.get_width() * self.tilt_factor)
        self.image = pygame.transform.smoothscale(self.original_image, (nw, self.original_image.get_height()))
        
        # Aplicar Fricción
        if self.acc.length_squared() == 0 and self.vel.length() > 0:
            friction_force = -self.vel.normalize() * self.friction
            self.acc += friction_force

        # Integración Física
        self.vel += self.acc * dt
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel * dt
        
        # Límites de pantalla
        self.pos.x = max(0, min(self.pos.x, width - self.rect.width))
        self.pos.y = max(0, min(self.pos.y, height - self.rect.height))
        
        self.rect.topleft = self.pos
        self.acc = Vector2(0, 0)