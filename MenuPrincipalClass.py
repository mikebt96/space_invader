import pygame
import sys
import os
from pygame import mixer

pygame.init()

class MenuPrincipal:
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    
    ANCHO = 800
    ALTO = 600
    
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Space Invaders")
    
    # Obtener la ruta del directorio del script o del bundle
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

    try:
        mixer.music.load(os.path.join(base_path, 'sounds', 'background_song1.mp3'))
    except:
        print("No se pudo cargar el sonido")
        pass
    try:
        mixer.music.play(-1)
    except:
        pass
    
    DIR_IMAGENES = os.path.join(base_path, "img")

    def __init__(self, init_game_mtd, init_score_mtd, init_about_mtd):
        self.init_game_mtd = init_game_mtd
        self.init_score_mtd = init_score_mtd
        self.init_about_mtd = init_about_mtd
        
    def cargar_imagen(self, nombre_archivo):
        ruta = os.path.join(self.DIR_IMAGENES, nombre_archivo)
        return pygame.image.load(ruta).convert_alpha()
    
    def mostrar_texto(self, texto, font, color, superficie, x, y):
        texto_objeto = font.render(texto, True, color)
        rectangulo_texto = texto_objeto.get_rect()
        rectangulo_texto.center = (x, y)
        superficie.blit(texto_objeto, rectangulo_texto)
        return rectangulo_texto
        
    def menu_principal(self):
        opciones = ["Iniciar Juego", "Puntajes", "Acerca De"]
        opcion_seleccionada = 0
        selector_rect = pygame.Rect(0, 0, 300, 50)
        
        fondo = self.cargar_imagen("menu_fondo.jpg")
        fondo = pygame.transform.scale(fondo, (self.ANCHO, self.ALTO))
        
        imagen = self.cargar_imagen("hybridge.gif")
        imagen = pygame.transform.scale(imagen, (80, 80))
        
        while True:
            self.ventana.blit(fondo, (0, 0))
            self.mostrar_texto("Space Invaders", pygame.font.Font(None, 64), self.BLANCO, self.ventana, self.ANCHO // 2, self.ALTO // 4)
            self.mostrar_texto("Hybridge", pygame.font.Font(None, 36), self.BLANCO, self.ventana, (self.ANCHO // 2), self.ALTO // 4 + 40)
            self.ventana.blit(imagen, (self.ANCHO // 2 - 40, self.ALTO // 4 + 60))
            
            rectangulos_texto = []
            
            for i, opcion in enumerate(opciones):
                rect_texto = self.mostrar_texto(opcion, pygame.font.Font(None, 32), self.BLANCO, self.ventana, self.ANCHO // 2, self.ALTO // 4 + 90 * (i + 1) + 100)
                rectangulos_texto.append(rect_texto)
                
            selector_rect.centerx = self.ANCHO // 2
            selector_rect.centery = rectangulos_texto[opcion_seleccionada].centery - 10
            pygame.draw.rect(self.ventana, self.ROJO, selector_rect, 2)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                    elif evento.key == pygame.K_DOWN:
                        opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                    elif evento.key == pygame.K_RETURN:
                        opcion_elegida = opciones[opcion_seleccionada]
                        print("opción seleccionada:", opcion_elegida)
                        if opcion_elegida.lower() == "iniciar juego":
                            self.init_game_mtd()
                            print("iniciar juego")
                            pygame.quit()
                        elif opcion_elegida.lower() == "puntajes":
                            self.init_score_mtd()
                            print("pantalla puntajes")
                            pygame.quit()
                        elif opcion_elegida.lower() == "acerca de":
                            self.init_about_mtd()
                            print("pantalla acerca de")
                            pygame.quit()
                        else:
                            print("otro")
            
            pygame.display.update()
        
# menu_principal = MenuPrincipal().menu_principal()
