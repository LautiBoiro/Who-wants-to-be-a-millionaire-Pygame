import pygame
from pygame.examples.cursors import image

import constantes
class Weapon():
    def __init__(self, image):
        self.image_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.image_original, self.angulo) #Rotación del arma segun el angulo
        self.forma = self.imagen.get_rect() #encapsula en un rectangulo la imagen

    def update(self, personaje):
        self.forma.center = personaje.shape.center #centramos el arma al centro del pj
        if personaje.flip == False:
            self.forma.x = self.forma.x + personaje.shape.width / 3
        if personaje.flip == True:
            self.forma.x = self.forma.x + personaje.shape.width / 3

        self.forma.y = self.forma.y + 10

    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.image_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.image_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)

    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)
        pygame.draw.rect(interfaz, constantes.COLOR_ARMA, self.forma, 1)

