import pygame
import random
import time
import sys
from Boton import crear_boton
from utils import salir_del_juego

# Configuraciones
ANCHO = 640
ALTO = 640
TAM_CUADRICULA = 4
TAM_CASILLA = ANCHO // TAM_CUADRICULA
TIEMPO_LIMITE = 60  # 1 minuto

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 100, 255)
ROJO = (255, 60, 60)
VERDE = (0, 180, 0)

def dividir_imagen(nombre_archivo):
    try:
        imagen_original = pygame.image.load(nombre_archivo)
        imagen_escalada = pygame.transform.scale(imagen_original, (ANCHO, ALTO))
        piezas = []
        for fila in range(TAM_CUADRICULA):
            fila_piezas = []
            for col in range(TAM_CUADRICULA):
                rect = pygame.Rect(col * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
                pieza = imagen_escalada.subsurface(rect).copy()
                fila_piezas.append(pieza)
            piezas.append(fila_piezas)
        return piezas
    except:
        colores = [(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)) for _ in range(16)]
        piezas = []
        for i in range(TAM_CUADRICULA):
            fila = []
            for j in range(TAM_CUADRICULA):
                superficie = pygame.Surface((TAM_CASILLA, TAM_CASILLA))
                superficie.fill(colores[i*TAM_CUADRICULA + j])
                fila.append(superficie)
            piezas.append(fila)
        return piezas

def crear_matriz():
    numeros = list(range(1, TAM_CUADRICULA**2 + 1))
    random.shuffle(numeros)
    return [[numeros[i*TAM_CUADRICULA + j] for j in range(TAM_CUADRICULA)] for i in range(TAM_CUADRICULA)]

def dibujar_matriz(ventana, matriz, seleccionadas, piezas_img, tiempo_restante):
    """Dibuja las piezas del rompecabezas en pantalla junto con el borde de selección y el tiempo restante."""

    for fila in range(TAM_CUADRICULA):
        for columna in range(TAM_CUADRICULA):
            numero_pieza = matriz[fila][columna] - 1  #Se le resta 1 para obtener un índice entre 0 y 15 (porque la matriz piezas_img está indexada desde 0)
            fila_img = numero_pieza // TAM_CUADRICULA
            columna_img = numero_pieza % TAM_CUADRICULA

            x = columna * TAM_CASILLA
            y = fila * TAM_CASILLA

            # Dibuja la imagen correspondiente a esa pieza
            ventana.blit(piezas_img[fila_img][columna_img], (x, y))

            # Si la pieza está seleccionada, usa un borde azul y más grueso
            if (fila, columna) in seleccionadas:
                color_borde = AZUL
                grosor = 4
            else:
                color_borde = NEGRO
                grosor = 2

            pygame.draw.rect(ventana, color_borde, (x, y, TAM_CASILLA, TAM_CASILLA), grosor)

    # Dibuja el tiempo restante en pantalla
    fuente = pygame.font.SysFont("Arial", 30)
    color_tiempo = ROJO if tiempo_restante < 10 else BLANCO
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_restante}s", True, color_tiempo)
    ventana.blit(texto_tiempo, (ANCHO - 150, ALTO + 10))
    # Dibuja el contador de piezas correctas usando la función recursiva
    piezas_bien = contar_piezas_correctas(matriz)
    texto_progreso = fuente.render(f"Piezas correctas: {piezas_bien}/16", True, VERDE)
    ventana.blit(texto_progreso, (20, ALTO + 10))



def ejecutar_minijuego(ventana_principal, config):
    ventana = pygame.display.set_mode((ANCHO, ALTO + 50))
    pygame.display.set_caption("Comodín: Rompecabezas")
    
    piezas_img = dividir_imagen("rompecabezas.png")
    matriz = crear_matriz()
    seleccionadas = []
    tiempo_inicio = time.time()
    gano = False
    
    fuente = pygame.font.SysFont("Arial", 24)
    boton_salir = crear_boton((150, 40), (ANCHO//2 , ALTO + 5), ventana, (255, 255, 255), "boton-normal.png")
    texto_salir = fuente.render("Salir", True, NEGRO)
    
    reloj = pygame.time.Clock()
    
    while True:
        tiempo_restante = max(0, TIEMPO_LIMITE - int(time.time() - tiempo_inicio))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if boton_salir["Rect"].collidepoint(pos):
                    pygame.display.set_mode((1280, 720))
                    return False
                
                if len(seleccionadas) < 2:
                    pos_pieza = obtener_posicion_click(pos)
                    if pos_pieza and pos_pieza not in seleccionadas:
                        seleccionadas.append(pos_pieza)
                    
                    if len(seleccionadas) == 2:
                        swap(matriz, seleccionadas[0], seleccionadas[1])
                        seleccionadas = []
        
        ventana.fill(NEGRO)
        dibujar_matriz(ventana, matriz, seleccionadas, piezas_img, tiempo_restante)
        ventana.blit(boton_salir["Superficie"], boton_salir["Rect"])
        ventana.blit(texto_salir, (boton_salir["Rect"].x + 50, boton_salir["Rect"].y + 10))
        pygame.display.flip()
        
        if matriz_ordenada(matriz):
            gano = True
            break
        
        if tiempo_restante <= 0:
            break
        
        reloj.tick(30)
    
    mostrar_resultado(ventana, gano)
    pygame.display.set_mode((1280, 720))
    return gano

def obtener_posicion_click(pos):
    x, y = pos
    return (y // TAM_CASILLA, x // TAM_CASILLA) if y < ALTO else None

def swap(matriz, p1, p2):
    """Intercambia los valores en las posiciones p1 y p2 de la matriz."""
    fila1, col1 = p1
    fila2, col2 = p2

    temporal = matriz[fila1][col1]
    matriz[fila1][col1] = matriz[fila2][col2]
    matriz[fila2][col2] = temporal


def matriz_ordenada(matriz):
    return all(matriz[i][j] == i*TAM_CUADRICULA + j + 1 for i in range(TAM_CUADRICULA) for j in range(TAM_CUADRICULA))

def mostrar_resultado(ventana, exito):
    ventana.fill(NEGRO)
    fuente = pygame.font.SysFont("Arial", 36)
    mensaje = fuente.render("¡Ganaste!" if exito else "¡Tiempo agotado!", True, VERDE if exito else ROJO)
    ventana.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 - 20))
    pygame.display.flip()
    pygame.time.delay(2000)

def contar_piezas_correctas(matriz, fila=0, columna=0) -> int:
    """Cuenta recursivamente cuántas piezas están en la posición correcta."""

    if fila >= TAM_CUADRICULA:
        return 0  # fin de la matriz

    # Verificamos si la pieza actual está en su lugar correcto
    valor_esperado = fila * TAM_CUADRICULA + columna + 1
    pieza_correcta = 1 if matriz[fila][columna] == valor_esperado else 0

    # Avanzamos a la siguiente posición
    if columna + 1 < TAM_CUADRICULA:
        return pieza_correcta + contar_piezas_correctas(matriz, fila, columna + 1)
    else:
        return pieza_correcta + contar_piezas_correctas(matriz, fila + 1, 0)
