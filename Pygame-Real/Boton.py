import pygame

def crear_boton(dimension, posicion, ventana, color_borde, imagen_normal, imagen_hover=None, imagen_presionado=None):
    boton = {
        "Ventana": ventana,
        "Dimension": dimension,
        "Posicion": posicion,
        "ColorBorde": color_borde,
        "Estado": "normal",
        "Superficie": pygame.image.load(imagen_normal).convert_alpha(),  # Mantenemos Superficie para compatibilidad
        "Imagenes": {
            "normal": pygame.image.load(imagen_normal).convert_alpha(),
            "hover": pygame.image.load(imagen_hover if imagen_hover else imagen_normal).convert_alpha(),
            "presionado": pygame.image.load(imagen_presionado if imagen_presionado else imagen_normal).convert_alpha()
        },
        "Rect": pygame.Rect(posicion, dimension)
    }
    # Escalar todas las imágenes
    for estado, img in boton["Imagenes"].items():
        boton["Imagenes"][estado] = pygame.transform.scale(img, dimension)
    boton["Superficie"] = pygame.transform.scale(boton["Superficie"], dimension)  # Escalar también la superficie
    return boton