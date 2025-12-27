import pygame
from pygame import mixer
from GameClass import Game
import os
import sys
from PlayerClass import Player
from EnemyClass import Enemy
from DrawingClass import Drawing
from PantallaNombreClass import PantallaNombre
from MenuPrincipalClass import MenuPrincipal
from AcercaDeMenuClass import MenuAcercaDe
from MenuPuntajesClass import MenuPuntajes

# Obtener la ruta del directorio del script o del bundle
base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

BACKGROUND = pygame.image.load(os.path.join(base_path, 'img', 'background.png'))
ICON_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'title_icon.png'))
TITLE = 'Space Invaders Hybridge'

PLAYER_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'player_image.png'))
BULLET_IMAGE = pygame.image.load(os.path.join(base_path, 'img', 'bullet_image.png'))

pygame.init()

WIDTH, HEIGTH = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption(TITLE)
pygame.display.set_icon(ICON_IMAGE)

try:
    mixer.music.load(os.path.join(base_path, 'sounds', 'background_song1.mp3'))
except:
    print("No se pudo cargar el sonido")
    pass

def main():
    puntaje = 0
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    try:
        mixer.music.play(-1)
    except:
        pass

    font = pygame.font.SysFont('comicsans', 50)
    game = Game(font, FPS, 3, WIN, WIDTH, HEIGTH, 0, clock)

    player_x = (WIDTH - PLAYER_IMAGE.get_width()) / 2
    player_y = 480
    player = Player(x=player_x, y=player_y, x_speed=5, y_speed=4)

    enemy_init = Enemy(speed=6)
    enemy_wave = 100
    enemies = enemy_init.create(enemy_wave)

    draw = Drawing(WIN)
    draw.drawing(game, player, enemies, FPS=60, puntos=puntaje)

    while run:
        clock.tick(FPS)

        if game.over():
            if puntaje > game.max_pun:
                sound = pygame.mixer.Sound(os.path.join(base_path, "sounds", "ganar.mp3"))
                sound.play()
                pantalla = PantallaNombre(puntaje, menu_principal)
                pygame.quit()
            else:
                menu_principal()
                run = False
            continue

        if game.escape():
            run = False
            continue

        if len(enemies) == 0:
            game.level += 1
            enemy_wave += 1
            enemy.increase_speed()
            player.increase_speed()
            enemies = enemy.create(amount=enemy_wave)
            if game.level % 3 == 0:
                if player.max_amount_bullets < 10:
                    player.max_amount_bullets += 1
                if game.lives < 6:
                    game.lives += 1

        player.move()
        player.create_bullets()
        game.reload_bullet(len(player.bullets))
        player.cooldown()

        for enemy in enemies:
            enemy.move()
            if player.hit(enemy):
                enemies.remove(enemy)
                player.fired_bullets.pop(0)
                crash_sound = pygame.mixer.Sound(os.path.join(base_path, "sounds", "explosion.wav"))
                pygame.mixer.Sound.play(crash_sound)
                puntaje += 1
            if enemy.y + enemy.get_height() >= HEIGTH:
                game.lives -= 1
                enemies.remove(enemy)

        draw.drawing(game, player, enemies, FPS, puntaje)

def initGame():
    main()

def initPuntaje():
    menu_puntajes = MenuPuntajes(menu_principal).ejecutar()

def initAbout():
    menu_acercade = MenuAcercaDe(menu_principal).ejecutar()

def menu_principal():
    print("menu principal")
    menu_principal = MenuPrincipal(initGame, initPuntaje, initAbout).menu_principal()

menu_principal()




