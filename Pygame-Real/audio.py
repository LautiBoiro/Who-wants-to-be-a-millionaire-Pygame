import pygame.mixer
from configuraciones import guardar_configuracion
def inicializar_audio(config):
    """Inicializa el sistema de audio usando la configuración"""
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=4, buffer=2048)
        pygame.mixer.set_num_channels(3)
        volumen = 0 if config.get('muteado', False) else config.get('volumen', 0.7)
        pygame.mixer.music.set_volume(volumen)
    except Exception as e:
        print(f"Error al inicializar audio: {e}")

def cargar_musicas():
    """Devuelve un diccionario con las rutas de los archivos de música"""
    return {
        'menu': 'opening.mp3',
        'inicio_juego': 'jugar.mp3',
        'preguntas_1_5': 'preguntas1-5.mp3',
        'preguntas_6_7': 'preguntas6-7.mp3',
        'victoria': 'preguntas6-7-ganar.mp3',
        'derrota': 'preguntas6-7-perder.mp3'
    }

def reproducir_musica(ruta, config, canal_prioridad=0, fade_ms=0, loops=None):
    """Reproduce música considerando la configuración actual"""
    try:
        volumen = 0 if config.get('muteado', False) else config.get('volumen', 0.7)
        
        if canal_prioridad == 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(loops=loops or (-1 if 'opening.mp3' in ruta else 0), fade_ms=fade_ms)
        else:
            sound = pygame.mixer.Sound(ruta)
            sound.set_volume(volumen)
            pygame.mixer.Channel(canal_prioridad).play(sound, loops=loops or 0, fade_ms=fade_ms)
        return True
    except Exception as e:
        print(f"Error al reproducir {ruta}: {e}")
        return False

def detener_musica(canal=None, fade_ms=0):
    """
    Detiene la música en el canal especificado
    """
    try:
        if canal == 0:
            pygame.mixer.music.fadeout(fade_ms)
        elif canal is None:
            for i in range(1, pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(i).fadeout(fade_ms)
        else:
            pygame.mixer.Channel(canal).fadeout(fade_ms)
    except Exception as e:
        print(f"Error al detener música: {e}")

def esta_sonando(canal=0):
    """
    Verifica si hay audio reproduciéndose en un canal
    """
    try:
        if canal == 0:
            return pygame.mixer.music.get_busy()
        return pygame.mixer.Channel(canal).get_busy()
    except Exception as e:
        print(f"Error al verificar estado de audio: {e}")
        return False

def ajustar_volumen(volumen, config, canal=None):
    """Ajusta el volumen y actualiza la configuración"""
    try:
        volumen = max(0.0, min(1.0, round(volumen, 1)))  # Asegura 0.0-1.0 con 1 decimal
        config['volumen'] = volumen
        config['muteado'] = False  # Al ajustar volumen, desmuteamos
        
        # Aplicar a todos los canales
        pygame.mixer.music.set_volume(volumen)
        if canal is None:
            for i in range(1, pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(i).set_volume(volumen)
        else:
            pygame.mixer.Channel(canal).set_volume(volumen)
        
        guardar_configuracion("config.json", config)
        return True
    except Exception as e:
        print(f"Error al ajustar volumen: {e}")
        return False

def alternar_mute(config):
    """Alterna el estado de mute y actualiza la configuración"""
    try:
        config['muteado'] = not config.get('muteado', False)
        volumen = 0 if config['muteado'] else config.get('volumen', 0.7)
        
        pygame.mixer.music.set_volume(volumen)
        for i in range(1, pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(volumen)
        
        guardar_configuracion("config.json", config)
        return config['muteado']
    except Exception as e:
        print(f"Error al alternar mute: {e}")
        return False

def detener_todo_audio():
    """Detiene TODA la música y sonidos en todos los canales"""
    try:
        pygame.mixer.music.stop()
        for i in range(1, pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).stop()
        print("Audio detenido completamente")
    except Exception as e:
        print(f"Error al detener todo el audio: {e}")