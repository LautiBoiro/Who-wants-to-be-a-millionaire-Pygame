import pygame
import random
import sys
from random import shuffle

# Importaciones del proyecto
from Boton import crear_boton
from comodin_rompecabezas import ejecutar_minijuego
from funciones_juego import guardar_estadistica, dibujar_pregunta_y_opciones
from recursos import inicializar_recursos, cargar_fondos
from estados import mostrar_derrota, mostrar_victoria, mostrar_retiro
from audio import reproducir_musica, detener_musica, detener_todo_audio
from utils import salir_del_juego

# =====================================================================
# FUNCIONES PURAS - CÁLCULOS Y TRANSFORMACIONES
# =====================================================================

def calcular_tiempo_restante(tiempo_inicio: int, tiempo_actual: int, 
                           tiempo_pausa_total: int, tiempo_limite: int) -> float:
    """Calcula el tiempo restante para responder una pregunta."""
    tiempo_transcurrido = (tiempo_actual - tiempo_inicio - tiempo_pausa_total) / 1000
    return max(0, tiempo_limite - tiempo_transcurrido)

def calcular_monto_retiro(nivel_actual: int) -> int:
    """Calcula el monto de retiro según el nivel actual."""
    premios = {3: 300000, 5: 600000, 7: 1200000}
    return premios.get(nivel_actual, 0)

def es_nivel_retiro(nivel: int) -> bool:
    """Verifica si el nivel permite retirarse."""
    return nivel in {3, 5}

def debe_cambiar_musica(nivel: int) -> bool:
    """Verifica si se debe cambiar la música en este nivel."""
    return nivel == 6

def crear_estado_tiempo_inicial(tiempo_inicio: int) -> dict:
    """Crea un estado inicial de tiempo."""
    return {
        'inicio': tiempo_inicio,
        'pausa_total': 0,
        'pausado': False,
        'pausa_inicio': 0
    }

def actualizar_tiempo_pausa(estado_tiempo: dict, tiempo_actual: int) -> dict:
    """Actualiza el tiempo de pausa acumulado."""
    nuevo_estado = estado_tiempo.copy()
    if estado_tiempo['pausado']:
        nuevo_estado['pausa_total'] += tiempo_actual - estado_tiempo['pausa_inicio']
        nuevo_estado['pausado'] = False
    return nuevo_estado

def crear_estado_partida_inicial() -> dict:
    """Crea el estado inicial de una partida."""
    return {
        'partidas_jugadas': 0,
        'preguntas_acertadas': 0,
        'tiempos_por_pregunta': [],
        'partidas_ganadas': 0,
        'mejor_tiempo': float('inf'),
        'comodin_disponible': True
    }

def actualizar_estado_partida(estado: dict, **kwargs) -> dict:
    """Actualiza el estado de la partida con nuevos valores."""
    nuevo_estado = estado.copy()
    nuevo_estado.update(kwargs)
    return nuevo_estado

def crear_resultado_pregunta(correcto: bool, tiempo_respuesta: float, 
                           indice_clickeado, comodin_usado: bool, 
                           timeout: bool) -> tuple:
    """Crea un resultado de pregunta estructurado."""
    return (correcto, (tiempo_respuesta, indice_clickeado), comodin_usado, timeout)

# =====================================================================
# FUNCIONES DE CONFIGURACIÓN Y RECURSOS
# =====================================================================

def cargar_imagen_escalada(ruta: str, tamaño: tuple) -> pygame.Surface:
    """Carga y escala una imagen."""
    imagen = pygame.image.load(ruta)
    if hasattr(imagen, 'convert_alpha'):
        imagen = imagen.convert_alpha()
    return pygame.transform.scale(imagen, tamaño)

def crear_boton_comodin() -> dict:
    """Crea el botón del comodín."""
    img_comodin = cargar_imagen_escalada("comodin-50-50.png", (80, 80))
    rect_comodin = img_comodin.get_rect(topleft=(895, 20))
    return {"Superficie": img_comodin, "Rect": rect_comodin}

def resetear_estados_botones(botones_respuesta: list) -> list:
    """Resetea el estado de todos los botones a 'normal' y restaura imágenes originales."""
    botones_actualizados = []
    for boton in botones_respuesta:
        boton_nuevo = boton.copy()
        boton_nuevo["Estado"] = "normal"
        
        # CLAVE: Restaurar las imágenes originales
        if "ImagenesOriginales" in boton_nuevo:
            boton_nuevo["Imagenes"] = boton_nuevo["ImagenesOriginales"].copy()
        
        botones_actualizados.append(boton_nuevo)
    return botones_actualizados

def obtener_tiempo_pregunta(config: dict) -> int:
    """Obtiene el tiempo límite para responder preguntas."""
    return config.get("tiempo_preguntas", 20)

# =====================================================================
# FUNCIONES DE INTERACCIÓN CON MOUSE
# =====================================================================

def actualizar_estado_hover_botones(botones_respuesta: list, 
                                   pos_mouse: tuple, 
                                   opciones: list) -> list:
    """Actualiza el estado hover de los botones según la posición del mouse."""
    botones_actualizados = []
    for i, boton in enumerate(botones_respuesta):
        boton_nuevo = boton.copy()
        if opciones[i] != "":
            if boton["Rect"].collidepoint(pos_mouse) and boton["Estado"] != "presionado":
                boton_nuevo["Estado"] = "hover"
            elif not boton["Rect"].collidepoint(pos_mouse) and boton["Estado"] not in ["normal", "presionado"]:
                boton_nuevo["Estado"] = "normal"
        botones_actualizados.append(boton_nuevo)
    return botones_actualizados

def detectar_click_boton(botones_respuesta: list, 
                        pos_click: tuple, 
                        opciones: list):
    """Detecta si se hizo click en algún botón válido y retorna su índice."""
    for j, boton in enumerate(botones_respuesta):
        if boton["Rect"].collidepoint(pos_click) and opciones[j] != "":
            return j
    return None

# =====================================================================
# FUNCIONES DE COMODÍN
# =====================================================================

def obtener_opciones_incorrectas(opciones: list, respuesta_correcta: str) -> list:
    """Obtiene los índices de las opciones incorrectas."""
    
    indices_incorrectos = []
    
    for i, opcion in enumerate(opciones):
        # Verifico que la opción no esté vacía y que su primer caracter no sea la respuesta correcta
        if opcion and opcion[0] != respuesta_correcta:
            indices_incorrectos.append(i)
    
    return indices_incorrectos

def crear_botones_vacios(botones_respuesta: list, 
                        indices_eliminar: list, 
                        ventana: pygame.Surface) -> list:
    """Crea botones vacíos para las opciones eliminadas."""
    botones_actualizados = []
    for i, boton in enumerate(botones_respuesta):
        if i in indices_eliminar:
            boton_vacio = crear_boton(
                (600, 50), 
                (100, 150 + i * 100), 
                ventana, 
                (0, 0, 0), 
                "boton-normal.png",
                "boton-confirmacion.png"
            )
            botones_actualizados.append(boton_vacio)
        else:
            botones_actualizados.append(boton)
    return botones_actualizados

def aplicar_comodin_50_50(pregunta: dict, 
                         botones_respuesta: list, 
                         ventana: pygame.Surface) -> tuple | list:
    """Aplica el comodín 50/50 eliminando dos opciones incorrectas."""
    pregunta_actualizada = pregunta.copy()
    
    # Guardar opciones originales si no existen
    if "opciones_originales" not in pregunta_actualizada:
        pregunta_actualizada["opciones_originales"] = pregunta["opciones"].copy()
    
    opciones_incorrectas = obtener_opciones_incorrectas(
        pregunta["opciones"], 
        pregunta["respuesta"]
    )
    
    if len(opciones_incorrectas) >= 2:
        opciones_a_eliminar = random.sample(opciones_incorrectas, 2)
        
        # Actualizar opciones
        nuevas_opciones = pregunta_actualizada["opciones"].copy()
        for i in opciones_a_eliminar:
            nuevas_opciones[i] = ""
        pregunta_actualizada["opciones"] = nuevas_opciones
        
        # Actualizar botones
        botones_actualizados = crear_botones_vacios(
            botones_respuesta, 
            opciones_a_eliminar, 
            ventana
        )
        
        return pregunta_actualizada, botones_actualizados
    
    return pregunta_actualizada, botones_respuesta

def procesar_comodin(ventana: pygame.Surface, config: dict, 
                    pregunta: dict, botones_respuesta: list, 
                    estado_tiempo: dict) -> tuple | list | dict:
    """Procesa el uso del comodín."""
    # Pausar tiempo
    nuevo_estado_tiempo = estado_tiempo.copy()
    nuevo_estado_tiempo['pausado'] = True
    nuevo_estado_tiempo['pausa_inicio'] = pygame.time.get_ticks()
    
    # Ejecutar minijuego
    resultado = ejecutar_minijuego(ventana, config)
    
    # Reanudar tiempo
    nuevo_estado_tiempo = actualizar_tiempo_pausa(nuevo_estado_tiempo, pygame.time.get_ticks())
    
    # Aplicar comodín si fue exitoso
    if resultado:
        pregunta_actualizada, botones_actualizados = aplicar_comodin_50_50(
            pregunta, botones_respuesta, ventana
        )
        return pregunta_actualizada, botones_actualizados, nuevo_estado_tiempo
    
    return pregunta, botones_respuesta, nuevo_estado_tiempo

# =====================================================================
# FUNCIONES DE RENDERIZADO
# =====================================================================

def renderizar_timeout(ventana: pygame.Surface, pregunta: dict, 
                      recursos: tuple, botones_respuesta: list, 
                      nivel_actual: int, config: dict) -> None:
    """Renderiza la pantalla de timeout."""
    fondo, fondo_pozo, fondo_descripcion, fuente = recursos
    fondo_juego = pygame.image.load("fondo.jpeg")
    
    ventana.blit(fondo_juego, (0, 0))
    
    dibujar_pregunta_y_opciones(
        ventana, pregunta, fuente, fondo, botones_respuesta, 
        nivel_actual, fondo_pozo, fondo_descripcion, 
        tiempo_restante=0, config=config
    )
    
    fondo_emergente = cargar_imagen_escalada("fondo-emergente.png", (600, 400))
    ventana.blit(fondo_emergente, (350, 153))
    
    fuente_grande = pygame.font.SysFont("Segoe UI Emoji", 32)
    texto = fuente_grande.render("Tiempo Agotado", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(640, 300))
    ventana.blit(texto, texto_rect)
    
    pygame.display.flip()
    pygame.time.delay(3000)

def renderizar_juego(ventana: pygame.Surface, pregunta: dict, 
                    recursos: tuple, botones_respuesta: list, 
                    nivel_actual: int, config: dict, 
                    tiempo_restante: float, mostrar_comodin: bool, 
                    boton_comodin: dict) -> None:
    """Renderiza la pantalla principal del juego."""
    fondo, fondo_pozo, fondo_descripcion, fuente = recursos
    fondo_juego = pygame.image.load("fondo.jpeg")
    
    ventana.blit(fondo_juego, (0, 0))
    
    if mostrar_comodin:
        ventana.blit(boton_comodin["Superficie"], boton_comodin["Rect"])
    
    dibujar_pregunta_y_opciones(
        ventana, pregunta, fuente, fondo, botones_respuesta, 
        nivel_actual, fondo_pozo, fondo_descripcion, 
        tiempo_restante=tiempo_restante, config=config
    )
    
    pygame.display.flip()

def obtener_indice_respuesta_correcta(pregunta: dict) -> int:
    """Obtiene el índice de la respuesta correcta."""
    if "opciones_originales" in pregunta:
        opciones_a_usar = pregunta["opciones_originales"]
    else:
        opciones_a_usar = pregunta["opciones"]

    for indice in range(len(opciones_a_usar)):
        opcion = opciones_a_usar[indice]
        if opcion and opcion[0] == pregunta["respuesta"]:
            return indice

    return -1


# =====================================================================
# FUNCIÓN PRINCIPAL DE PROCESAMIENTO DE PREGUNTA
# =====================================================================

def procesar_pregunta(ventana: pygame.Surface, pregunta: dict, recursos: tuple, botones_respuesta: list, inicio_pregunta: int, nivel_actual: int, comodin_disponible: bool, config: dict) -> tuple:
    """Procesa una pregunta individual del juego."""
    
    # Configuración inicial
    tiempo_pregunta = obtener_tiempo_pregunta(config)
    estado_tiempo = crear_estado_tiempo_inicial(pygame.time.get_ticks())
    boton_comodin = crear_boton_comodin()
    
    # Estados del juego
    comodin_usado = False
    botones_respuesta = resetear_estados_botones(botones_respuesta)
    pregunta_actual = pregunta.copy()
    
    # Bucle principal
    while True:
        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante = calcular_tiempo_restante(
            estado_tiempo['inicio'], tiempo_actual, 
            estado_tiempo['pausa_total'], tiempo_pregunta
        )
        
        # Verificar timeout
        if tiempo_restante <= 0 and not estado_tiempo['pausado']:
            renderizar_timeout(ventana, pregunta_actual, recursos, botones_respuesta, nivel_actual, config)
            return crear_resultado_pregunta(False, 0, None, comodin_usado, True)
        
        # Actualizar hover de botones
        pos_mouse = pygame.mouse.get_pos()
        botones_respuesta = actualizar_estado_hover_botones(
            botones_respuesta, pos_mouse, pregunta_actual["opciones"]
        )
        
        # Renderizar juego
        mostrar_comodin = comodin_disponible and not comodin_usado
        renderizar_juego(
            ventana, pregunta_actual, recursos, botones_respuesta, 
            nivel_actual, config, tiempo_restante, mostrar_comodin, boton_comodin
        )
        
        # Procesar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # Click en comodín
                if mostrar_comodin and boton_comodin["Rect"].collidepoint(pos):
                    pregunta_actual, botones_respuesta, estado_tiempo = procesar_comodin(
                        ventana, config, pregunta_actual, botones_respuesta, estado_tiempo
                    )
                    comodin_usado = True
                    continue
                
                # Click en botón de respuesta
                indice_clickeado = detectar_click_boton(botones_respuesta, pos, pregunta_actual["opciones"])
                if indice_clickeado is not None:
                    botones_respuesta[indice_clickeado]["Estado"] = "presionado"
                    pygame.display.flip()
                    pygame.time.delay(100)
                    
                    tiempo_respuesta = (pygame.time.get_ticks() - inicio_pregunta) / 1000
                    es_correcta = pregunta_actual["opciones"][indice_clickeado][0] == pregunta_actual["respuesta"]
                    
                    return crear_resultado_pregunta(es_correcta, tiempo_respuesta, indice_clickeado, comodin_usado, False)

# =====================================================================
# FUNCIONES DE GESTIÓN DE MÚSICA
# =====================================================================

def gestionar_musica_nivel(nivel_actual: int, musicas: dict, config: dict) -> None:
    """Gestiona el cambio de música según el nivel."""
    if debe_cambiar_musica(nivel_actual):
        detener_musica(canal=1)
        reproducir_musica(musicas['preguntas_6_7'], config, canal_prioridad=1)

def reproducir_musica_inicial(musicas: dict, config: dict) -> None:
    """Reproduce la música inicial del juego."""
    reproducir_musica(musicas['preguntas_1_5'], config, canal_prioridad=1)

def reproducir_musica_derrota(musicas: dict, config: dict) -> None:
    """Reproduce la música de derrota."""
    detener_todo_audio()
    reproducir_musica(musicas['derrota'], config, canal_prioridad=1, loops=0)

def reproducir_musica_victoria(musicas: dict, config: dict) -> None:
    """Reproduce la música de victoria."""
    detener_todo_audio()
    reproducir_musica(musicas['victoria'], config, canal_prioridad=1, loops=0)

# =====================================================================
# FUNCIONES DE PANTALLAS DE RESULTADO
# =====================================================================

def mostrar_pantalla_derrota(ventana: pygame.Surface, pregunta: dict, recursos: tuple, botones_respuesta: list, indice_clickeado, timeout: bool, nivel_actual: int, config: dict) -> None:
    """Muestra la pantalla de derrota con la respuesta correcta."""
    indice_correcto = obtener_indice_respuesta_correcta(pregunta)
    
    ventana.blit(pygame.image.load("fondo.jpeg"), (0, 0))
    
    if indice_correcto != -1:
        respuesta_correcta = indice_correcto
    else:
        respuesta_correcta = None

    if timeout:
        respuesta_incorrecta = None
    else:
        respuesta_incorrecta = indice_clickeado
    
    dibujar_pregunta_y_opciones(ventana, pregunta, recursos[3], recursos[0],botones_respuesta, nivel_actual, recursos[1],recursos[2], respuesta_correcta,respuesta_incorrecta, config=config)
    
    pygame.time.delay(1000)

def mostrar_pantalla_respuesta_correcta(ventana: pygame.Surface, pregunta: dict, recursos: tuple, botones_respuesta: list, nivel_actual: int, config: dict) -> None:
    """Muestra la pantalla de respuesta correcta."""
    indice_correcto = obtener_indice_respuesta_correcta(pregunta)
    
    dibujar_pregunta_y_opciones(
        ventana, pregunta, recursos[3], recursos[0],
        botones_respuesta, nivel_actual, recursos[1],
        recursos[2], respuesta_correcta=indice_correcto,
        mostrar_descripcion=True, config=config
    )
    pygame.time.delay(2000)

# =====================================================================
# FUNCIONES DE RETIRO
# =====================================================================

def crear_boton_retiro(posicion: tuple, ventana: pygame.Surface) -> dict:
    """Crea un botón para la opción de retiro."""
    return crear_boton(
        (200, 60), posicion, ventana, (0, 0, 0), 
        "boton-normal.png", "boton-confirmacion.png"
    )

def renderizar_pantalla_retiro(ventana: pygame.Surface, fuente: pygame.font.Font) -> tuple | dict:
    """Renderiza la pantalla de opción de retiro."""
    fondo_emergente = cargar_imagen_escalada("fondo-emergente.png", (600, 400))
    ventana.blit(fondo_emergente, (350, 153))
    
    fuente_grande = pygame.font.SysFont("Segoe UI Emoji", 32)
    texto = fuente_grande.render("¿Retirarse con el premio?", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(640, 300))
    ventana.blit(texto, texto_rect)
    
    boton_si = crear_boton_retiro((430, 400), ventana)
    boton_no = crear_boton_retiro((660, 400), ventana)
    
    ventana.blit(boton_si["Imagenes"]["normal"], boton_si["Rect"])
    ventana.blit(boton_no["Imagenes"]["normal"], boton_no["Rect"])
    
    texto_si = fuente.render("Sí", True, (255, 255, 255))
    texto_no = fuente.render("No", True, (255, 255, 255))
    ventana.blit(texto_si, (boton_si["Rect"].x + 90, boton_si["Rect"].y + 15))
    ventana.blit(texto_no, (boton_no["Rect"].x + 80, boton_no["Rect"].y + 15))
    
    pygame.display.flip()
    
    return boton_si, boton_no

def mostrar_opcion_retiro(ventana: pygame.Surface, clock: pygame.time.Clock, fuente: pygame.font.Font, config: dict) -> bool:
    """Muestra la opción de retiro y retorna la decisión del jugador."""
    boton_si, boton_no = renderizar_pantalla_retiro(ventana, fuente)
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_si["Rect"].collidepoint(evento.pos):
                    return True
                elif boton_no["Rect"].collidepoint(evento.pos):
                    return False
        clock.tick(60)
    
    return False

# =====================================================================
# FUNCIÓN PRINCIPAL DE JUEGO
# =====================================================================

def actualizar_estadisticas_partida(estado_partida: dict, tiempo_total = None) -> dict:
    """Actualiza las estadísticas de la partida."""
    nuevo_estado = estado_partida.copy()
    
    if tiempo_total is not None:
        nuevo_estado['tiempos_por_pregunta'].append(tiempo_total)
        if tiempo_total < nuevo_estado['mejor_tiempo']:
            nuevo_estado['mejor_tiempo'] = tiempo_total
    
    return nuevo_estado

def procesar_resultado_pregunta(ventana: pygame.Surface, pregunta: dict, recursos: tuple, botones_respuesta: list, resultado: tuple, nivel_actual: int, config: dict, musicas: dict, estado_partida: dict, nombre_usuario: str, modo: str) -> tuple:
    """Procesa el resultado de una pregunta."""
    
    is_correct, (tiempo_respuesta, indice_clickeado), comodin_usado, timeout = resultado
    
    if comodin_usado:
        comodin_disponible = False
    else:
        comodin_disponible = estado_partida['comodin_disponible']

    nuevo_estado = actualizar_estado_partida(
        estado_partida,
        comodin_disponible=comodin_disponible
    )
    
    nuevo_estado['tiempos_por_pregunta'].append(tiempo_respuesta)
    
    if timeout or not is_correct:
        reproducir_musica_derrota(musicas, config)
        
        mostrar_pantalla_derrota(ventana, pregunta, recursos, botones_respuesta, indice_clickeado, timeout, nivel_actual, config)
        
        guardar_estadistica(nombre_usuario, modo, nuevo_estado['partidas_jugadas'], nuevo_estado['preguntas_acertadas'],nuevo_estado['tiempos_por_pregunta'],nuevo_estado['partidas_ganadas'], nuevo_estado['mejor_tiempo'])
            
        if not timeout:
            respuesta_incorrecta = indice_clickeado
        else:
            respuesta_incorrecta = None

        respuesta_correcta = None  # Siempre es None en este contexto
        tupla_respuestas = (respuesta_incorrecta, respuesta_correcta)
        eleccion = mostrar_derrota(ventana, pregunta, recursos, botones_respuesta,tupla_respuestas ,musicas, config)
        
        if eleccion == "reiniciar":
            detener_todo_audio()
            return "reiniciar", nuevo_estado
        else:
            detener_musica(canal=2)
            return "volver_menu", nuevo_estado
    else:
        nuevo_estado = actualizar_estado_partida(nuevo_estado, preguntas_acertadas=nuevo_estado['preguntas_acertadas'] + 1)
        
        mostrar_pantalla_respuesta_correcta(ventana, pregunta, recursos, botones_respuesta, nivel_actual, config)
        
        return "continuar", nuevo_estado

def jugar_partida(ventana: pygame.Surface, clock: pygame.time.Clock, preguntas: list, nombre_usuario: str, modo: str, config: dict, fuente: pygame.font.Font, musicas: dict) -> str:
    """Ejecuta una partida del juego."""
    
    fondos = cargar_fondos()
    
    while True:
        recursos, botones_respuesta = inicializar_recursos(ventana)
        reproducir_musica_inicial(musicas, config)
        
        estado_partida = crear_estado_partida_inicial()
        estado_partida = actualizar_estado_partida(estado_partida, partidas_jugadas=1)
        
        shuffle(preguntas)
        inicio_ronda = pygame.time.get_ticks()
        gano = True
        
        for i, pregunta in enumerate(preguntas):
            nivel_actual = i + 1
            
            gestionar_musica_nivel(nivel_actual, musicas, config)
            
            inicio_pregunta = pygame.time.get_ticks()
            
            resultado = procesar_pregunta(
                ventana, pregunta, recursos, botones_respuesta,
                inicio_pregunta, nivel_actual, 
                estado_partida['comodin_disponible'], config
            )
            
            accion, estado_partida = procesar_resultado_pregunta(
                ventana, pregunta, recursos, botones_respuesta, resultado,
                nivel_actual, config, musicas, estado_partida, 
                nombre_usuario, modo
            )
            
            if accion == "reiniciar":
                break
            elif accion == "volver_menu":
                return "volver_menu"
            
            # Verificar opción de retiro
            if es_nivel_retiro(nivel_actual):
                if mostrar_opcion_retiro(ventana, clock, fuente, config):
                    monto_acumulado = calcular_monto_retiro(nivel_actual)
                    mostrar_retiro(ventana, recursos, monto_acumulado, config)
                    
                    guardar_estadistica(nombre_usuario, modo, estado_partida['partidas_jugadas'],estado_partida['preguntas_acertadas'], estado_partida['tiempos_por_pregunta'],estado_partida['partidas_ganadas'], estado_partida['mejor_tiempo'])
                    
                    return "volver_menu"
        
        # Verificar victoria
        if gano and estado_partida['preguntas_acertadas'] == len(preguntas):
            reproducir_musica_victoria(musicas, config)
            
            tiempo_total = (pygame.time.get_ticks() - inicio_ronda) / 1000
            estado_partida = actualizar_estadisticas_partida(estado_partida, tiempo_total)
            estado_partida = actualizar_estado_partida(estado_partida, partidas_ganadas=1)
            
            guardar_estadistica(nombre_usuario, modo, estado_partida['partidas_jugadas'],estado_partida['preguntas_acertadas'], estado_partida['tiempos_por_pregunta'],estado_partida['partidas_ganadas'], estado_partida['mejor_tiempo'])
            
            mostrar_victoria(ventana, recursos, musicas, config)
            return "volver_menu"
        
        clock.tick(60)
