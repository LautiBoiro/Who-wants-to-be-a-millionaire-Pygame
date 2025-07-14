import pygame
import json
from Boton import crear_boton

def cargar_configuracion(path):
    """Carga la configuración desde JSON con valores por defecto"""
    config_default = {
        "caracteres_maximo": 14,
        "cantidad_preguntas": 7,
        "tiempo_preguntas": 20,
        "volumen": 1.0,
        "brillo": 0.7,
        "muteado": False,
        "daltonismo": {
            "activado": False,
            "tipo": "protanopia",
            "simbolos": True
        }
    }
    
    try:
        with open(path, "r") as archivo:
            config_usuario = json.load(archivo)
            # Combinar con valores por defecto para nuevas propiedades
            config_usuario["daltonismo"] = {**config_default["daltonismo"], **config_usuario.get("daltonismo", {})}
            return {**config_default, **config_usuario}
    except:
        return config_default

def guardar_configuracion(path, config):
    """Guarda la configuración en JSON"""
    try:
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump(config, archivo, indent=4)
        return True
    except Exception as e:
        print(f"Error al guardar configuración: {e}")
        return False

def crear_botones_opciones():
    """Crea botones con rectángulos de colisión precisos"""
    botones = {
        # Botones de volumen
        "bajar_volumen": {
            "Superficie": pygame.transform.scale(pygame.image.load("boton-bajar-volumen.png"), (50, 50)),
            "Rect": pygame.Rect(430, 250, 50, 50)  # X,Y coinciden con extremo izquierdo barra
        },
        "subir_volumen": {
            "Superficie": pygame.transform.scale(pygame.image.load("boton-subir-volumen.png"), (50, 50)),
            "Rect": pygame.Rect(780, 250, 50, 50)  # X,Y coinciden con extremo derecho barra
        },
        # Botón volver
        "volver": {
            "Superficie": pygame.transform.scale(pygame.image.load("boton-salir.png"), (250, 50)),
            "Rect": pygame.Rect(515, 580, 250, 50)
        }
    }
    return botones