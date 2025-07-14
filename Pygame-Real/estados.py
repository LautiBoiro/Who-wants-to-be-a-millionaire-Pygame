import pygame
import sys
from Boton import crear_boton
from funciones_juego import dibujar_pregunta_y_opciones
from audio import reproducir_musica, detener_todo_audio
from utils import salir_del_juego

def cargar_fuente(tamanio):
    try:
        return pygame.font.Font("copperplategothicbold.ttf", tamanio)
    except:
        return pygame.font.SysFont("Segoe UI Emoji", tamanio)

def mostrar_derrota(ventana, pregunta, recursos, botones, indices, musicas, config):
    """Muestra la pantalla de derrota con opción de reintentar"""
    fondo, fondo_pozo, fondo_descripcion, fuente = recursos
    indice_clickeado, indice_correcto = indices
    
    # 1. Configurar imágenes según daltonismo
    daltonismo_activado = config.get("daltonismo", {}).get("activado", False)
    tipo_daltonismo = config.get("daltonismo", {}).get("tipo", "protanopia") if daltonismo_activado else None
    
    if indice_correcto is not None:
        img_correcta = f"boton-{tipo_daltonismo}-correcto.png" if daltonismo_activado else "boton-normal-verde.png"
        try:
            img = pygame.image.load(img_correcta).convert_alpha()
            # SOLO cambiar la imagen normal, NO tocar la hover
            botones[indice_correcto]["Imagenes"]["normal"] = pygame.transform.scale(img, botones[indice_correcto]["Dimension"])
        except:
            img = pygame.image.load("boton-normal-verde.png").convert_alpha()
            # SOLO cambiar la imagen normal, NO tocar la hover
            botones[indice_correcto]["Imagenes"]["normal"] = pygame.transform.scale(img, botones[indice_correcto]["Dimension"])

    # 2. Dibujar la escena base (pregunta y respuestas)
    ventana.blit(pygame.image.load("fondo.jpeg"), (0, 0))
    
    dibujar_pregunta_y_opciones(ventana,pregunta, fuente, fondo, botones, 0,fondo_pozo, fondo_descripcion,respuesta_correcta=indice_correcto,respuesta_incorrecta=indice_clickeado,config=config)

    # 3. Dibujar fondo emergente SIN overlay semitransparente
    fondo_emergente = pygame.transform.scale(pygame.image.load("fondo-emergente.png"), (600, 400))
    ventana.blit(fondo_emergente, (340, 160))

    # 4. Dibujar elementos del emergente directamente
    fuente_grande = cargar_fuente(36)
    texto = fuente_grande.render("Has perdido. ¿Deseás reintentar?", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(640, 300))
    ventana.blit(texto, texto_rect)

    # 5. Botones Sí/No (simplificado)
    boton_si = crear_boton((200, 60), (430, 400), ventana, (255, 255, 255), "boton-normal.png")
    texto_si = fuente.render("Sí", True, (255, 255, 255))
    
    boton_no = crear_boton((200, 60), (660, 400), ventana, (255, 255, 255), "boton-normal.png")
    texto_no = fuente.render("No", True, (255, 255, 255))
    
    ventana.blit(boton_si["Superficie"], boton_si["Rect"])
    ventana.blit(texto_si, (boton_si["Rect"].x + 90, boton_si["Rect"].y + 15))
    
    ventana.blit(boton_no["Superficie"], boton_no["Rect"])
    ventana.blit(texto_no, (boton_no["Rect"].x + 80, boton_no["Rect"].y + 15))

    pygame.display.flip()

    # 6. Manejo de eventos
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if boton_si["Rect"].collidepoint(pos):
                    return "reiniciar"
                elif boton_no["Rect"].collidepoint(pos):
                    return "salir"
        pygame.time.delay(100)

    return None

def mostrar_victoria(ventana, recursos, musicas, config):
    detener_todo_audio()
    
    # Cargar fuentes con borde para mejor legibilidad
    fuente_titulo = cargar_fuente(48)
    fuente_premio = cargar_fuente(72)
    
    # Reproducir música de victoria
    reproducir_musica(musicas['victoria'], config, canal_prioridad=1, loops=0)
    
    # Cargar animaciones
    frames_confeti = []
    frames_boton = []
    
    # Precargar frames de confeti (0-30)
    for i in range(31):
        try:
            frame = pygame.image.load(f"framesparticulas/gif-ganar-{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (1280, 720))  # Asegurar tamaño
            frames_confeti.append(frame)
        except:
            print(f"Frame confeti {i} no encontrado")
            break
    
    # Precargar frames de botón dorado (1-30)
    for i in range(1, 31):
        try:
            frame = pygame.image.load(f"framesbotondorado/frame_{i}-ezgif.com-gif-to-apng-converter.png").convert_alpha()
            # Escalar si es necesario (ajustar según tus imágenes)
            frame = pygame.transform.scale(frame, (600, 150))  
            frames_boton.append(frame)
        except:
            print(f"Frame botón {i} no encontrado")
            break
    
    # Control de animación
    frame_actual_confeti = 0
    frame_actual_boton = 0
    ultimo_cambio = pygame.time.get_ticks()
    fps_animacion = 15
    
    # Botón de salir (posicionado más abajo)
    boton_salir = crear_boton((300, 70), (490, 600), ventana, (255, 255, 255), "boton-salir.png")
    
    # Posiciones definidas como constantes
    POSICIONES = {
        'titulo': 170,
        'subtitulo': 230,
        'premio': 360,  # Posición más baja para el premio
        'boton_dorado': 400  # Posición del botón dorado
    }
    
    corriendo = True
    while corriendo:
        tiempo_actual = pygame.time.get_ticks()
        
        # Actualizar animaciones
        if tiempo_actual - ultimo_cambio > 1000 // fps_animacion:
            frame_actual_confeti = (frame_actual_confeti + 1) % len(frames_confeti)
            frame_actual_boton = (frame_actual_boton + 1) % len(frames_boton)
            ultimo_cambio = tiempo_actual
        
        dibujar_y_renderizar_victoria(ventana,POSICIONES, frames_confeti, frame_actual_confeti, frames_boton, frame_actual_boton, fuente_titulo, fuente_premio, boton_salir)
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_salir["Rect"].collidepoint(evento.pos):
                    corriendo = False
                    detener_todo_audio()
                    return

def mostrar_retiro(ventana, recursos, monto_acumulado,config):
    detener_todo_audio()
    
    # Cargar fuentes
    fuente_titulo = cargar_fuente(48)
    fuente_premio = cargar_fuente(72)
    
    # Cargar animación de confeti
    frames_confeti = []
    for i in range(31):
        try:
            frame = pygame.image.load(f"framesparticulas/gif-ganar-{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (1280, 720))
            frames_confeti.append(frame)
        except:
            print(f"Frame confeti {i} no encontrado")
            break
    
    # Cargar imagen de confirmación
    try:
        boton_confirmacion = pygame.image.load("boton-confirmacion.png").convert_alpha()
        boton_confirmacion = pygame.transform.scale(boton_confirmacion, (600, 150))  # Ajustar tamaño
    except:
        print("No se pudo cargar boton-confirmacion.png")
        boton_confirmacion = None
    
    # Control de animación
    frame_actual_confeti = 0
    ultimo_cambio = pygame.time.get_ticks()
    fps_animacion = 15
    
    # Botón de salir
    boton_salir = crear_boton((300, 70), (490, 600), ventana, (255, 255, 255), "boton-salir.png")
    
    # Posiciones definidas como constantes
    POSICIONES = {
        'titulo': 170,
        'subtitulo': 230,
        'premio': 360,
        'boton_confirmacion': 400
    }
    
    # Formatear monto
    monto_str = "${:,.0f}".format(monto_acumulado).replace(",", ".")
    
    corriendo = True
    while corriendo:
        tiempo_actual = pygame.time.get_ticks()
        
        # Actualizar animación de confeti
        if tiempo_actual - ultimo_cambio > 1000 // fps_animacion:
            frame_actual_confeti = (frame_actual_confeti + 1) % len(frames_confeti)
            ultimo_cambio = tiempo_actual
        
        # --- Dibujado ---
        # 1. Fondo estático
        ventana.blit(pygame.image.load("fondo.jpeg"), (0, 0))
        
        # 3. Botón de confirmación (estático)
        if boton_confirmacion:
            boton_rect = boton_confirmacion.get_rect(center=(640, POSICIONES['boton_confirmacion']))
            ventana.blit(boton_confirmacion, boton_rect)
        
        # 4. Textos con sombras
        # Sombra de textos
        texto_sombra_titulo = fuente_titulo.render("¡FELICIDADES!", True, (0, 0, 0))
        ventana.blit(texto_sombra_titulo, (1280//2 - texto_sombra_titulo.get_width()//2 + 3, POSICIONES['titulo'] + 3))
        
        texto_sombra_subtitulo = fuente_titulo.render("TE RETIRASTE CON", True, (0, 0, 0))
        ventana.blit(texto_sombra_subtitulo, (1280//2 - texto_sombra_subtitulo.get_width()//2 + 3, POSICIONES['subtitulo'] + 3))
        
        texto_sombra_premio = fuente_premio.render(monto_str, True, (0, 0, 0))
        ventana.blit(texto_sombra_premio, (1280//2 - texto_sombra_premio.get_width()//2 + 3, POSICIONES['premio'] + 3))
        
        # Textos principales
        texto_titulo = fuente_titulo.render("¡FELICIDADES!", True, (255, 255, 255))
        ventana.blit(texto_titulo, (1280//2 - texto_titulo.get_width()//2, POSICIONES['titulo']))
        
        texto_subtitulo = fuente_titulo.render("TE RETIRASTE CON", True, (255, 255, 255))
        ventana.blit(texto_subtitulo, (1280//2 - texto_subtitulo.get_width()//2, POSICIONES['subtitulo']))
        
        texto_premio = fuente_premio.render(monto_str, True, (255, 215, 0))  # Dorado
        ventana.blit(texto_premio, (1280//2 - texto_premio.get_width()//2, POSICIONES['premio']))
        
        # 5. Botón de salir
        ventana.blit(boton_salir["Superficie"], boton_salir["Rect"])
        
        pygame.display.flip()
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_salir["Rect"].collidepoint(evento.pos):
                    corriendo = False
                    detener_todo_audio()
                    return


def dibujar_y_renderizar_victoria(ventana,POSICIONES, frames_confeti, frame_actual_confeti, frames_boton, frame_actual_boton, fuente_titulo, fuente_premio, boton_salir):
    # --- Dibujado ---
        # 1. Fondo estático
        ventana.blit(pygame.image.load("fondo.jpeg"), (0, 0))
        
        # 2. Confeti (como capa base)
        if frames_confeti:
            ventana.blit(frames_confeti[frame_actual_confeti], (0, 0))
        
        # 3. Botón dorado (ANTES del texto del premio)
        if frames_boton:
            boton_rect = frames_boton[frame_actual_boton].get_rect(center=(640, POSICIONES['boton_dorado']))
            ventana.blit(frames_boton[frame_actual_boton], boton_rect)
        
        # 4. Textos (SOBRE el botón dorado)
        # Primero dibujamos las sombras
        texto_sombra_ganaste = fuente_titulo.render("¡FELICIDADES!", True, (0, 0, 0))
        ventana.blit(texto_sombra_ganaste, (1280//2 - texto_sombra_ganaste.get_width()//2 + 3, POSICIONES['titulo'] + 3))
        
        texto_sombra_subtitulo = fuente_titulo.render("GANASTE EL PREMIO MAYOR", True, (0, 0, 0))
        ventana.blit(texto_sombra_subtitulo, (1280//2 - texto_sombra_subtitulo.get_width()//2 + 3, POSICIONES['subtitulo'] + 3))
        
        texto_sombra_premio = fuente_premio.render("$1.200.000", True, (0, 0, 0))
        ventana.blit(texto_sombra_premio, (1280//2 - texto_sombra_premio.get_width()//2 + 3, POSICIONES['premio'] + 3))
        
        # Luego dibujamos los textos principales (sobre las sombras)
        texto_ganaste = fuente_titulo.render("¡FELICIDADES!", True, (255, 255, 255))
        ventana.blit(texto_ganaste, (1280//2 - texto_ganaste.get_width()//2, POSICIONES['titulo']))
        
        texto_subtitulo = fuente_titulo.render("GANASTE EL PREMIO MAYOR", True, (255, 255, 255))
        ventana.blit(texto_subtitulo, (1280//2 - texto_subtitulo.get_width()//2, POSICIONES['subtitulo']))
        
        texto_premio = fuente_premio.render("$1.200.000", True, (255, 215, 0))  # Dorado
        ventana.blit(texto_premio, (1280//2 - texto_premio.get_width()//2, POSICIONES['premio']))
        
        # 5. Botón de salir (siempre visible)
        ventana.blit(boton_salir["Superficie"], boton_salir["Rect"])
        
        pygame.display.flip()
