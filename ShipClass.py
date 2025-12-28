import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        super().__init__()
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        # La máscara permite colisiones píxel por píxel (Nivel Pro)
        self.mask = None 
        # El rect es obligatorio para que el Sprite se dibuje
        self.rect = None 

    def draw(self, window):
        # Si tienes un rect, es mejor usarlo para el blit
        if self.ship_img and self.rect:
            window.blit(self.ship_img, self.rect)