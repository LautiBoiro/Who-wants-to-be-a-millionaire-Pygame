import pygame
from Boton import crear_boton

def cargar_fuente(tamanio):
    try:
        return pygame.font.Font("copperplategothicbold.ttf", tamanio)
    except:
        return pygame.font.SysFont("Segoe UI Emoji", tamanio)

def cargar_fondos():
    """Carga todos los fondos necesarios"""
    return {
        'menu': pygame.transform.scale(pygame.image.load("fondo.jpeg"), (1280, 720)),
        'respuestas': pygame.transform.scale(pygame.image.load("fondo-respuestas.png"), (900, 720)),
        'pozo': pygame.transform.scale(pygame.image.load("fondo-pozo.png"), (300, 600)),
        'descripcion': pygame.transform.scale(pygame.image.load("fondo-descripcion.png"), (830, 125)),
        'emergente': pygame.transform.scale(pygame.image.load("fondo-emergente.png"), (600, 400)),
        'victoria': pygame.transform.scale(pygame.image.load("boton-confirmacion.png"), (1280, 720)),
        'logo': pygame.transform.scale(pygame.image.load("logo.png"), (325, 325))
    }

def inicializar_recursos(ventana):
    """Retorna (fondos, fuente), botones"""
    recursos = (
        pygame.transform.scale(pygame.image.load("fondo-respuestas.png"), (900, 720)),
        pygame.transform.scale(pygame.image.load("fondo-pozo.png"), (300, 600)),
        pygame.transform.scale(pygame.image.load("fondo-descripcion.png"), (830, 125)),
        cargar_fuente(28)
    )
    
    botones_respuesta = []
    for i in range(4):
        boton = crear_boton_con_backup(
            (600, 50), 
            (100, 150 + i * 100), 
            ventana, 
            (0, 0, 0), 
            "boton-normal.png",
            "boton-confirmacion.png"
        )
        botones_respuesta.append(boton)
    
    return recursos, botones_respuesta

def crear_boton_con_backup(dimension, posicion, ventana, color, img_normal, img_hover="boton-confirmacion.png"):
    """Crea un botón guardando copias de las imágenes originales."""
    boton = crear_boton(dimension, posicion, ventana, color, img_normal, img_hover)
    
    # Guardar copia de las imágenes originales
    boton["ImagenesOriginales"] = {
        "normal": boton["Imagenes"]["normal"].copy(),
        "hover": boton["Imagenes"]["hover"].copy()
    }
    
    return boton