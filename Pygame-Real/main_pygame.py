import pygame
import sys
from menu import iniciar_bucle_juego
from configuraciones import cargar_configuracion
from audio import inicializar_audio

def main():
    pygame.init()
    VENTANA = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("¿Quién quiere ser millonario?")
    clock = pygame.time.Clock()
    
    # Cargar configuración e inicializar audio
    config = cargar_configuracion("config.json")
    inicializar_audio(config)
    
    iniciar_bucle_juego(VENTANA, clock, config)  # Pasar config al juego

if __name__ == "__main__":
    main()