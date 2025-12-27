import pygame
import sys
import os
import webbrowser


class MenuAcercaDe:

    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    GRIS = (200, 200, 200)
    ROJO = (255, 0, 0)


    ANCHO = 800
    ALTO = 600
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Acerca De")

    def __init__(self, back_mtd):
        self.back_mtd = back_mtd

    def cargar_imagen(self, nombre_archivo):
        # Obtener la ruta del directorio del script y construir la ruta a la imagen
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        ruta = os.path.join(base_path, 'img', nombre_archivo)
        return pygame.image.load(ruta).convert_alpha()

    def mostrar_texto(self, texto, font, color, superficie, x, y):
        texto_objeto = font.render(texto, True, color)
        rectangulo_texto = texto_objeto.get_rect()
        rectangulo_texto.topleft = (x, y)
        superficie.blit(texto_objeto, rectangulo_texto)

    def dibujar_boton(self, texto, font, color, superficie, x, y, ancho, alto):
        pygame.draw.rect(superficie, color, (x, y, ancho, alto))
        texto_ancho, texto_alto = font.size(texto)
        texto_x = x + (ancho - texto_ancho) // 2
        texto_y = y + (alto - texto_alto) // 2
        self.mostrar_texto(texto, font, self.NEGRO, superficie, texto_x, texto_y)

    def mostrar_contenido(self, contenido, font_contenido, y_offset):
        espacio_horizontal_disponible = self.ANCHO - 100  # Espacio horizontal disponible para el contenido
        for linea in contenido.split('\n'):
            palabras = linea.split()
            texto_linea = ""
            for palabra in palabras:
                texto_linea_temp = texto_linea + palabra + " "
                texto_ancho_temp = font_contenido.size(texto_linea_temp)[0]
                if texto_ancho_temp < espacio_horizontal_disponible:
                    texto_linea = texto_linea_temp
                else:
                    self.mostrar_texto(texto_linea.strip(), font_contenido, self.BLANCO, self.ventana, (self.ANCHO - font_contenido.size(texto_linea.strip())[0]) // 2, y_offset)
                    y_offset += font_contenido.size(texto_linea.strip())[1]
                    texto_linea = palabra + " "
            self.mostrar_texto(texto_linea.strip(), font_contenido, self.BLANCO, self.ventana, (self.ANCHO - font_contenido.size(texto_linea.strip())[0]) // 2, y_offset)
            y_offset += font_contenido.size(texto_linea.strip())[1]

    def mostrar_menu(self):
        self.ventana.fill(self.NEGRO)
        fondo = self.cargar_imagen("menu_fondo.jpg")
        fondo = pygame.transform.scale(fondo, (self.ANCHO, self.ALTO))
        self.ventana.blit(fondo, (0, 0))

        titulo_texto = "Acerca De"
        titulo_font = pygame.font.Font(None, 48)
        titulo_ancho = titulo_font.size(titulo_texto)[0]
        titulo_x = (self.ANCHO - titulo_ancho) // 2
        self.mostrar_texto(titulo_texto, titulo_font, self.BLANCO, self.ventana, titulo_x, 50)

        subtitulo_texto = "Space Invaders Hybridge"
        subtitulo_font = pygame.font.Font(None, 36)
        subtitulo_ancho = subtitulo_font.size(subtitulo_texto)[0]
        subtitulo_x = (self.ANCHO - subtitulo_ancho) // 2
        self.mostrar_texto(subtitulo_texto, subtitulo_font, self.BLANCO, self.ventana, subtitulo_x, 120)

        contenido = "¡Explora la galaxia y aprende Programación Orientada a Objetos (POO) con nuestro emocionante Space Invaders!\nCada nave, cada disparo, ¡todo es un objeto interactivo! Únete a nosotros para una experiencia divertida y educativa en este emocionante cruce de juego y aprendizaje.\n¡Prepárate para salvar el universo!"
        font_contenido = pygame.font.Font(None, 30)
        y_offset = max(200, subtitulo_font.size(subtitulo_texto)[1] + 120)  
        self.mostrar_contenido(contenido, font_contenido, y_offset)

        texto_enlace = "¡Haz clic aquí para visitar Hybridge!"
        font_enlace = pygame.font.Font(None, 30)
        enlace_ancho = font_enlace.size(texto_enlace)[0]
        enlace_x = (self.ANCHO - enlace_ancho) // 2
        self.mostrar_texto(texto_enlace, font_enlace, self.ROJO, self.ventana, enlace_x, 500)

        pygame.draw.rect(self.ventana, self.GRIS, (20, 20, 50, 50))
        self.dibujar_boton("<", pygame.font.Font(None, 36), self.GRIS, self.ventana, 20, 20, 50, 50)

        pygame.display.update()

    def ejecutar(self):
        self.mostrar_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if 20 <= x <= 70 and 20 <= y <= 70:
                            print("acción atrás")
                            self.back_mtd()
                        elif 300 <= y <= 520:
                            webbrowser.open("https://hybridge.education")


# pygame.init()

# men_acerca_de = MenuAcercaDe()
# men_acerca_de.ejecutar()
