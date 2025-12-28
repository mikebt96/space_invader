import pygame
import os
from PlayerClass import Player
from EnemyClass import Enemy

class Game:
    def __init__(self, window, assets, width, height):
        self.window = window
        self.assets = assets
        self.width, self.height = width, height
        self.state = "MENU" 
        
        # Audio
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        # Highscores y Nombre
        self.highscore_file = "puntajes.txt"
        self.highscores = self.load_highscores()
        self.player_name = ""
        
        self.reset_game()

    def load_highscores(self):
        if not os.path.exists(self.highscore_file):
            return [("AAA", 0)] * 5
        
        scores = []
        try:
            with open(self.highscore_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if "," in line: # Verificamos que exista la coma
                        parts = line.split(",")
                        if len(parts) == 2:
                            name, score = parts
                            scores.append((name, int(score)))
            
            # Si el archivo estaba vacío o corrupto, rellenamos
            if not scores:
                return [("AAA", 0)] * 5
                
            return sorted(scores, key=lambda x: x[1], reverse=True)[:5]
            
        except Exception as e:
            print(f"⚠️ Error leyendo puntajes: {e}")
            return [("AAA", 0)] * 5

    def save_score(self):
        self.highscores.append((self.player_name if self.player_name else "AAA", self.score))
        self.highscores = sorted(self.highscores, key=lambda x: x[1], reverse=True)[:5]
        with open(self.highscore_file, "w") as f:
            for n, s in self.highscores:
                f.write(f"{n},{s}\n")

    def reset_game(self):
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player(self.width//2, self.height-100, self.assets['player'], self.bullets, self.assets['bullet'])
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.score = 0
        self.level = 0
        self.player_name = ""

    def update(self, dt):
        if self.state == "PLAYING":
            if len(self.enemies) == 0:
                self.level += 1
                img_dict = {'blue': (self.assets['e_blue'], self.assets['s_blue']),
                            'green': (self.assets['e_green'], self.assets['s_green']),
                            'purple': (self.assets['e_purple'], self.assets['s_purple'])}
                self.enemies.add(Enemy.create_wave(3 + self.level*2, self.width, img_dict, self.level))

            self.player_group.update(dt, self.width, self.height)
            self.bullets.update(dt)
            self.enemies.update(dt)
            
            hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
            if hits:
                self.score += len(hits) * 10
                self.assets['sfx_explosion'].set_volume(self.sfx_volume)
                self.assets['sfx_explosion'].play()
            
            if pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask):
                self.state = "ENTER_NAME"

    def draw(self):
        self.window.blit(self.assets['bg'], (0,0))
        
        if self.state == "MENU":
            self.draw_text("ANTIGRAVITY 2026", 80, self.width//2, 150)
            self.draw_text("ENTER - JUGAR | P - PUNTAJES | V - VOLUMEN", 30, self.width//2, 400)

        elif self.state == "VOLUME_MENU":
            self.draw_text("AUDIO", 60, self.width//2, 150)
            # Barra Música
            self.draw_text(f"MUSICA: {int(self.music_volume*100)}%", 30, self.width//2, 250)
            pygame.draw.rect(self.window, (100, 100, 100), (self.width//2 - 100, 280, 200, 20))
            pygame.draw.rect(self.window, (0, 255, 255), (self.width//2 - 100, 280, 200 * self.music_volume, 20))
            self.draw_text("FLECHAS PARA AJUSTAR | M - VOLVER", 20, self.width//2, 500)

        elif self.state == "ENTER_NAME":
            self.draw_text("¡NUEVO RECORD!", 60, self.width//2, 150)
            self.draw_text(f"ESCRIBE TU NOMBRE: {self.player_name}_", 40, self.width//2, 300)
            self.draw_text("PRESIONA ENTER PARA GUARDAR", 20, self.width//2, 450)

        elif self.state == "HIGHSCORES":
            self.draw_text("TOP 5 PILOTOS", 60, self.width//2, 100)
            for i, (name, score) in enumerate(self.highscores):
                self.draw_text(f"{name} ...... {score} PTS", 40, self.width//2, 200 + (i*50))
            self.draw_text("M - VOLVER", 25, self.width//2, 530)

        elif self.state == "PLAYING":
            self.bullets.draw(self.window)
            self.enemies.draw(self.window)
            self.player_group.draw(self.window)
            self.draw_text(f"SCORE: {self.score}", 30, 80, 30)

    def draw_text(self, text, size, x, y):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        surf = font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=(x, y))
        self.window.blit(surf, rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "MENU":
                if event.key == pygame.K_RETURN: self.state = "PLAYING"
                if event.key == pygame.K_p: self.state = "HIGHSCORES"
                if event.key == pygame.K_v: self.state = "VOLUME_MENU"
            
            elif self.state == "VOLUME_MENU":
                if event.key == pygame.K_RIGHT: self.music_volume = min(1.0, self.music_volume + 0.1)
                if event.key == pygame.K_LEFT: self.music_volume = max(0.0, self.music_volume - 0.1)
                pygame.mixer.music.set_volume(self.music_volume)
                if event.key == pygame.K_m: self.state = "MENU"

            elif self.state == "ENTER_NAME":
                if event.key == pygame.K_RETURN:
                    self.save_score()
                    self.state = "HIGHSCORES"
                elif event.key == pygame.K_BACKSPACE: self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 3: self.player_name += event.unicode.upper()

            elif self.state == "HIGHSCORES":
                if event.key == pygame.K_m: self.state = "MENU"

            elif self.state == "PLAYING":
                if event.key == pygame.K_SPACE: self.player.shoot()
                
            