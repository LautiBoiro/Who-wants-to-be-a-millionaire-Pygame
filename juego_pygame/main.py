import pygame  # Importo la librería de pygame
import constantes  # Traigo las constantes del otro archivo
from personaje import Personaje  # Traigo la clase Personaje
from weapons import Weapon

pygame.init()  # Inicio el juego

window = pygame.display.set_mode((constantes.WIDTH_VENTANA, constantes.HEIGHT_VENTANA))
pygame.display.set_caption("Celeste")  # Poner nombre del juego para que aparezca arriba en la ventana

def escalar_img(image, scale):  # Creo una función para escalar las imágenes y no ser redundante
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# Cargar animaciones / importar imagenes
#personaje
animaciones = []
for i in range(1, 8):
    try:
        img = pygame.image.load(f"assets/images/characters/correr({i}).png")
        img = escalar_img(img, constantes.ESCALA_PERSONAJE)
        animaciones.append(img)
    except pygame.error as e:
        print(f"Error cargando la imagen correr({i}).png: {e}")

#Arma
imagen_machete = pygame.image.load(f"assets//images//weapons//machete.png")
imagen_machete = escalar_img(imagen_machete, constantes.ESCALA_ARMA)

#crear un jugador ded la clase personaje
jugador = Personaje(50, 540, animaciones)

#crear un arma de la clase weapon
machete = Weapon(imagen_machete)

# Variables de movimiento del jugador
mover_izquierda = False
mover_derecha = False
mover_arriba = False
mover_abajo = False

# Controlar el frame rate
reloj = pygame.time.Clock()

run = True
while run == True:
    reloj.tick(constantes.FPS)  # 60 FPS
    window.fill(constantes.COLOR_BG)

    # Calculo del movimiento
    delta_x = (-constantes.VELOCIDAD if mover_izquierda else 0) + (constantes.VELOCIDAD if mover_derecha else 0)
    delta_y = (-constantes.VELOCIDAD if mover_arriba else 0) + (constantes.VELOCIDAD if mover_abajo else 0)

    jugador.update() #aca llamo al metodo que cambia los frames del jugador

    #actualiza el estado del arma
    machete.update(jugador)

    jugador.movimiento(delta_x, delta_y)
    #dibujar al jugador
    jugador.draw(window)

    #dibujar el arma
    machete.dibujar(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Cerrar el juego
            run = False

        if event.type == pygame.KEYDOWN:  # Tecla presionada
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

        if event.type == pygame.KEYUP:  # Tecla soltada
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    pygame.display.update()

pygame.quit()