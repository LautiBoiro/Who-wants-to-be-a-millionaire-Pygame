import pygame
import constantes

class Personaje():
    def __init__(self, x, y, animaciones):  #determino donde quiero que spawnee el pj
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0  #frame en el que se esta mostrando al personaje
        self.update_time = pygame.time.get_ticks()  #Me guarda cuántos ms pasaron desde que abrí pygame
        self.image = animaciones[self.frame_index] #Imagen de la animación que se esta mostrando actualmente
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)

    def update(self):
        cooldown_animacion = 100  # CD de 100 ms de cuanto tiempo pasa de frame a frame (Frame de Personaje)
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion: #si el timpo que pasó aca es mayor a 100ms, actualiza el frame
            self.frame_index += 1 #Cambia el frame del personaje en 1 imagen por cada 100ms
            if self.frame_index >= len(self.animaciones):  #Verifica que si el frame actual llega al final vuelve al primero (frame 0) para así crear un bucle con los frames
                self.frame_index = 0
            self.image = self.animaciones[self.frame_index]
            self.update_time = pygame.time.get_ticks() #actualiza la variable update time para que sea igual al tiempo actual

    def draw(self, interfaz):  #Dónde queremos dibujar al pj
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(image_flip, self.shape)
        pygame.draw.rect(interfaz, constantes.COLOR_PERSONAJE, self.shape, 1)

    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:  #Si me muevo hacia la izquierda, se da vuelta
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x += delta_x
        self.shape.y += delta_y