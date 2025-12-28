import pygame
import sys
import os
from GameClass import Game

WIDTH, HEIGHT = 800, 600

# Esta es la función que causó el error, ahora está unificada
def get_path(*parts):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)

def load_assets():
    a = {}
    try:
        # --- IMÁGENES ---
        a['bg'] = pygame.image.load(get_path('img', 'background.png')).convert()
        a['player'] = pygame.image.load(get_path('img', 'player_image.png')).convert_alpha()
        a['bullet'] = pygame.image.load(get_path('img', 'bullet_image.png')).convert_alpha()
        a['e_blue'] = pygame.image.load(get_path('img', 'enemy_blue_image.png')).convert_alpha()
        a['e_green'] = pygame.image.load(get_path('img', 'enemy_green_image.png')).convert_alpha()
        a['e_purple'] = pygame.image.load(get_path('img', 'enemy_purple_image.png')).convert_alpha()
        a['s_blue'] = pygame.image.load(get_path('img', 'shot_blue.png')).convert_alpha()
        a['s_green'] = pygame.image.load(get_path('img', 'shot_green.png')).convert_alpha()
        a['s_purple'] = pygame.image.load(get_path('img', 'shot_purple.png')).convert_alpha()
        
        # --- AUDIO ---
        # Efecto de explosión
        a['sfx_explosion'] = pygame.mixer.Sound(get_path('sounds', 'explosion.wav'))
        
        # MÚSICA DE FONDO (Corregido a background_song.mp3)
        pygame.mixer.music.load(get_path('sounds', 'background_song.mp3'))
        a['music_loaded'] = True
        
        print("✅ Todo cargado correctamente: Imágenes y background_song.mp3")
        
    except Exception as e:
        print(f"⚠️ Nota: No se pudo cargar algún recurso: {e}")
        # Si falló la música pero las imágenes están bien, permitimos seguir
        if 'bg' not in a:
            return None
        a['music_loaded'] = a.get('music_loaded', False)
        
    return a
    
def main():
    # Inicialización del audio con settings de baja latencia
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()
    
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Antigravity 2026")
    clock = pygame.time.Clock()
    
    assets = load_assets()
    
    # Si los assets no se cargaron, cerramos para no dar errores de música
    if assets is None:
        print("El juego no puede iniciar sin los archivos de imagen o sonido.")
        pygame.quit()
        sys.exit()
    
    # Iniciar música de fondo
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    game = Game(WIN, assets, WIDTH, HEIGHT)

    while True:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Gestión de entradas para menús
            game.handle_input(event)

        game.update(dt)
        game.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()