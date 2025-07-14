import pygame
import sys
from funciones_juego import dibujar_pregunta_y_opciones  # ✅ Necesario
from utils import salir_del_juego

def procesar_pregunta(ventana, pregunta, recursos, botones, inicio_pregunta, indice_actual, config):
    """Retorna (is_correct, (tiempo_respuesta, indice_clickeado))"""
    fondo, fondo_pozo, fondo_descripcion, fuente = recursos
    
    responder = True
    
    while responder:
        ventana.blit(pygame.image.load("fondo.jpeg"), (0, 0))
        dibujar_pregunta_y_opciones(ventana, pregunta, fuente, fondo, botones, indice_actual, fondo_pozo, fondo_descripcion, config=config)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for j, boton in enumerate(botones):
                    if boton["Rect"].collidepoint(pos):
                        letra_correcta = pregunta["respuesta"]
                        letra_clickeada = pregunta["opciones"][j][0]
                        indice_clickeado = j  # Guardar el índice clickeado
                        
                        for k, opcion in enumerate(pregunta["opciones"]):
                            if opcion[0] == letra_correcta:
                                indice_correcto = k
                                break
                        
                        tiempo_respuesta = (pygame.time.get_ticks() - inicio_pregunta) / 1000
                        return (letra_clickeada == letra_correcta, (tiempo_respuesta, indice_clickeado))
    
    return (False, (0, None))  # Retorna 2 valores