import pygame
import sys
import emoji
from juego import jugar_partida
from recursos import cargar_fondos
from funciones_archivos import cargar_preguntas 
from funciones_genericas_archivos import cargar_configuracion, leer_estadisticas
from funciones_juego import seleccionar_preguntas_por_dificultad 
from Boton import crear_boton
from audio import inicializar_audio, cargar_musicas, reproducir_musica, detener_musica, ajustar_volumen, alternar_mute
from configuraciones import guardar_configuracion, crear_botones_opciones
from utils import salir_del_juego


def cargar_fuente(tamaño):
    try:
        return pygame.font.Font("copperplategothicbold.ttf", tamaño)
    except:
        return pygame.font.SysFont("Segoe UI Emoji", tamaño)

def iniciar_bucle_juego(ventana, clock, config):
    inicializar_audio(config)
    musicas = cargar_musicas()
    reproducir_musica(musicas['menu'], config)
    
    max_caracteres = config.get("caracteres_maximo", 20)
    
    fondos = cargar_fondos()
    fuente = cargar_fuente(28)
    
    while True:
        if mostrar_menu_principal(ventana, clock, fondos, fuente, max_caracteres, config, musicas):
            break
    
    salir_del_juego(config)

def mostrar_menu_principal(ventana, clock, fondos, fuente, max_caracteres, config, musicas):
    """Muestra el menú principal del juego"""
    inicializar_audio(config)
    
    botones_menu = crear_botones_menu_principal(ventana)

    reproducir_musica(musicas['menu'], config, canal_prioridad=0)

    while True:
        # Limpiar pantalla completamente
        ventana.fill((0, 0, 0))
        ventana.blit(fondos['menu'], (0, 0))
        ventana.blit(fondos['logo'], (475, 15))

        # Dibujar botones del menú (usando Superficie para compatibilidad)
        for boton in botones_menu.values():
            ventana.blit(boton["Superficie"], boton["Rect"])

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if botones_menu["jugar"]["Rect"].collidepoint(pos):
                    iniciar_juego(config, ventana, clock, fondos, fuente, max_caracteres, musicas)
                
                elif botones_menu["opciones"]["Rect"].collidepoint(pos):
                    pygame.event.clear()
                    mostrar_menu_opciones(ventana, clock, fondos, fuente, config)
                    pygame.event.clear()
                    continue
                
                elif botones_menu["estadisticas"]["Rect"].collidepoint(pos):
                    pygame.event.clear()
                    mostrar_estadisticas(ventana, clock, fondos, config)
                    pygame.event.clear()
                    continue
                
                elif botones_menu["salir"]["Rect"].collidepoint(pos):
                    detener_musica()
                    return True
        
        pygame.display.flip()
        clock.tick(60)

def mostrar_menu_nombre(ventana, clock, fondos, fuente, max_caracteres, musicas, config):
    nombre_usuario = pedir_nombre_usuario(ventana, clock, fondos, fuente, max_caracteres, config)
    return nombre_usuario

def mostrar_menu_dificultad(ventana, clock, fondos, fuente, nombre_usuario, config, musicas):
    opciones_dificultad = {
        "Facil": (380, 250),
        "Normal": (380, 330),
        "Dificil": (380, 410),
        "Extremo": (380, 490)
    }

    boton_salir = crear_boton((150, 45), (30, 20), ventana, (255, 255, 255), "boton-salir.png")
    botones_dificultad = {}

    for texto, (x, y) in opciones_dificultad.items():
        boton = crear_boton((500, 60), (x, y), ventana, (255, 255, 255), "boton-normal.png")
        botones_dificultad[texto] = boton

    dificultad_seleccionada = None
    salir_seleccion = False
    
    while not salir_seleccion and dificultad_seleccionada is None:
        ventana.blit(fondos['menu'], (0, 0))
        ventana.blit(fondos['descripcion'], (235, 115))
        
        titulo = fuente.render("Selecciona una dificultad", True, (255, 255, 255))
        ventana.blit(titulo, (1280//2 - titulo.get_width()//2, 150))
        
        for texto, boton in botones_dificultad.items():
            ventana.blit(boton["Superficie"], boton["Rect"])
            texto_render = fuente.render(texto, True, (255, 255, 255))
            ventana.blit(texto_render, (boton["Rect"].x + 200, boton["Rect"].y + 15))
        
        ventana.blit(boton_salir["Superficie"], boton_salir["Rect"])
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if boton_salir["Rect"].collidepoint(pos):
                    salir_seleccion = True
                for texto, boton in botones_dificultad.items():
                    if boton["Rect"].collidepoint(pos):
                        dificultad_seleccionada = texto.lower()
                        break
        
        clock.tick(60)
    
    return dificultad_seleccionada

def mostrar_menu_opciones(ventana, clock, fondos, fuente, config):
    """Muestra el menú de opciones con nuevo layout"""
    botones = crear_botones_opciones()
    
    # Fuente para los títulos
    fuente_titulo = pygame.font.SysFont("Arial", 36, bold=True)
    
    # Botones para daltonismo
    boton_daltonismo = crear_boton((385, 50), (440, 380), ventana, (255, 255, 255), "boton-normal.png")
    boton_tipo_daltonismo = crear_boton((330, 50), (470, 440), ventana, (255, 255, 255), "boton-normal.png")
    boton_simbolos = crear_boton((385, 50), (440, 500), ventana, (255, 255, 255), "boton-normal.png")
    
    
    esperando = True
    while esperando:
        ventana.fill((0, 0, 0))
        ventana.blit(fondos['menu'], (0, 0))
        # Título principal
        titulo = fuente_titulo.render("CONFIGURACIÓN", True, (255, 255, 255))
        ventana.blit(titulo, (1280//2 - titulo.get_width()//2, 100))
        
        manejar_botones_opciones(config, ventana, boton_daltonismo, boton_tipo_daltonismo, boton_simbolos, fuente, botones)
        
        # Manejo de eventos (se mantiene igual)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                esperando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                
                pos = pygame.mouse.get_pos()
                
                if boton_daltonismo["Rect"].collidepoint(pos):
                    config["daltonismo"]["activado"] = not config["daltonismo"]["activado"]
                    guardar_configuracion("config.json", config)
                
                elif config["daltonismo"]["activado"] and boton_tipo_daltonismo["Rect"].collidepoint(pos):
                    # Rotar entre los tipos de daltonismo
                    tipos = ["protanopia", "deuteranopia", "tritanopia"]
                    indice_actual = tipos.index(config["daltonismo"]["tipo"])
                    nuevo_indice = (indice_actual + 1) % len(tipos) #Se calcula cual es el indice siguiente
                    config["daltonismo"]["tipo"] = tipos[nuevo_indice]
                    guardar_configuracion("config.json", config)
                
                elif config["daltonismo"]["activado"] and boton_simbolos["Rect"].collidepoint(pos):
                    config["daltonismo"]["simbolos"] = not config["daltonismo"]["simbolos"]
                    guardar_configuracion("config.json", config)
                    
                elif botones["volver"]["Rect"].collidepoint(pos):
                    esperando = False
                
                
                elif botones["subir_volumen"]["Rect"].collidepoint(pos):
                    nuevo_volumen = min(1.0, round(config.get('volumen', 0.7) + 0.1, 1))
                    ajustar_volumen(nuevo_volumen, config)
                
                elif botones["bajar_volumen"]["Rect"].collidepoint(pos):
                    nuevo_volumen = max(0.0, round(config.get('volumen', 0.7) - 0.1, 1))
                    ajustar_volumen(nuevo_volumen, config)
                
                guardar_configuracion("config.json", config)  # Guardar inmediatamente
        
        guardar_configuracion("config.json", config)
        pygame.display.flip()
        clock.tick(60)

def mostrar_estadisticas(ventana, clock, fondos, config, scroll_y=0, max_scroll=None):
    """Muestra las estadísticas de forma recursiva"""
    fuente = cargar_fuente(30)
    fuente_titulo = cargar_fuente(30)
    fuente_encabezado = cargar_fuente(22)
    fuente_dato = cargar_fuente(20)

    columnas = ["Usuario", "Partidas", "Acertadas", "Prom.Tiempo", "Ganadas", "Mejor Tiempo"]
    margen_izquierdo = 60
    espacio_entre_col = 180

    boton_volver = crear_boton((150, 45), (30, 20), ventana, (255, 255, 255), "boton-salir.png")

    # Cargar datos solo en la primera llamada
    if max_scroll is None:
        datos = {}
        for dif in ["facil", "normal", "dificil", "extremo"]:
            datos[dif] = leer_estadisticas(f"estadisticas_{dif}.csv")

        
        # Calcular el máximo scroll necesario
        temp_y = 80
        for dif in ["facil", "normal", "dificil", "extremo"]:
            temp_y += 40  # Título
            temp_y += 30  # Encabezados
            if not datos[dif]:
                temp_y += 40  # Mensaje "Sin estadísticas"
            else:
                temp_y += len(datos[dif]) * 25  # Filas de datos
            temp_y += 50  # Espacio entre secciones
        
        altura_necesaria = temp_y
        area_visible = 720
        max_scroll = max(0, altura_necesaria - area_visible)
    else: 
        datos = {}  
        for dificultad in ["facil", "normal", "dificil", "extremo"]:
            archivo = f"estadisticas_{dificultad}.csv"
            estadisticas = leer_estadisticas(archivo)
            datos[dificultad] = estadisticas 

    # Dibujar contenido
    ventana.blit(fondos['menu'], (0, 0))
    y = 80 + scroll_y

    for dif in ["facil", "normal", "dificil", "extremo"]:
        titulo = fuente_titulo.render(dif.capitalize(), True, (255, 255, 0))
        rect_titulo = titulo.get_rect(center=(1280 // 2, y))
        ventana.blit(titulo, rect_titulo)
        y += 40

        for i, col in enumerate(columnas):
            encabezado = fuente_encabezado.render(col, True, (200, 200, 200))
            ventana.blit(encabezado, (margen_izquierdo + i * espacio_entre_col, y))
        y += 30

        if not datos[dif]:
            texto = fuente_dato.render("Sin estadísticas registradas", True, (255, 100, 100))
            rect = texto.get_rect(center=(1280 // 2, y + 30))
            ventana.blit(texto, rect)
            y += 40
        else:
            for est in datos[dif]:
                fila = [
                    est["Usuario"],
                    str(est["Partidas_jugadas"]),
                    str(est["Preguntas_acertadas"]),
                    f"{est['Tiempo_promedio']}s",
                    str(est["Contador_partidas_ganadas"]),
                ]
                if est["Mejor_tiempo"] == float("inf"):
                    fila.append("--")
                else:
                    fila.append(f"{est['Mejor_tiempo']}s")
                    
                for i, valor in enumerate(fila):
                    texto = fuente_dato.render(valor, True, (255, 255, 255))
                    ventana.blit(texto, (margen_izquierdo + i * espacio_entre_col, y))
                y += 25
        y += 50
    
    ventana.blit(boton_volver["Superficie"], boton_volver["Rect"])
    pygame.display.flip()

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            salir_del_juego(config)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return
            elif evento.key == pygame.K_DOWN:
                return mostrar_estadisticas(ventana, clock, fondos, config, max(scroll_y - 20, -max_scroll), max_scroll)
            elif evento.key == pygame.K_UP:
                return mostrar_estadisticas(ventana, clock, fondos, config, min(scroll_y + 20, 0), max_scroll)
        elif evento.type == pygame.MOUSEWHEEL:
            return mostrar_estadisticas(ventana, clock, fondos, config, max(min(scroll_y + evento.y * 30, 0), -max_scroll), max_scroll)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver["Rect"].collidepoint(evento.pos):
                return

    clock.tick(60)
    return mostrar_estadisticas(ventana, clock, fondos, config, scroll_y, max_scroll)

def pedir_nombre_usuario(ventana, clock, fondos, fuente, max_caracteres, config):
    input_activo = True
    texto_input = ""
    
    boton_input = crear_boton((400, 60), (440, 300), ventana, (255, 255, 255), "boton-normal.png")
    boton_salir = crear_boton((150, 45), (30, 20), ventana, (255, 255, 255), "boton-salir.png")

    while input_activo:
        manejar_mostrar_nombre_usuario(ventana, fondos, boton_input, boton_salir, texto_input, fuente)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_del_juego(config)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if boton_salir["Rect"].collidepoint(pos):
                    return None
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if texto_input.strip() != "":
                        return texto_input.strip()
                    else:
                        input_activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                elif len(texto_input) < max_caracteres:
                    texto_input += evento.unicode

        clock.tick(60)
    
    return None

def dibujar_texto(ventana, texto, x, y, fuente, color=(255, 255, 255)):
    render = fuente.render(emoji.emojize(texto, language="alias"), True, color)
    ventana.blit(render, (x, y))

def manejar_opciones_daltonismo(config, ventana, boton_daltonismo,boton_tipo_daltonismo, boton_simbolos, fuente):
    # Sección de daltonismo
    texto_daltonismo = fuente.render("ACCESIBILIDAD PARA DALTONISMO", True, (255, 255, 255))
    ventana.blit(texto_daltonismo, (1280//2 - texto_daltonismo.get_width()//2, 330))
    
    # Botón activar/desactivar daltonismo
    daltonismo_activado = config["daltonismo"]["activado"]

    if daltonismo_activado:
        estado_daltonismo = "  ACTIVADO"
    else:
        estado_daltonismo = "DESACTIVADO"
    texto_boton_dalton = fuente.render(f"Daltonismo: {estado_daltonismo}", True, (255, 255, 255))
    ventana.blit(boton_daltonismo["Superficie"], boton_daltonismo["Rect"])
    ventana.blit(texto_boton_dalton, (boton_daltonismo["Rect"].x + 30, boton_daltonismo["Rect"].y + 15))
    
    # Botón tipo de daltonismo (solo visible si está activado)
    if config["daltonismo"]["activado"]:
        tipo = config["daltonismo"]["tipo"].upper()
        texto_boton_tipo = fuente.render(f"Tipo:  {tipo}", True, (255, 255, 255))
        ventana.blit(boton_tipo_daltonismo["Superficie"], boton_tipo_daltonismo["Rect"])
        ventana.blit(texto_boton_tipo, (boton_tipo_daltonismo["Rect"].x + 30, boton_tipo_daltonismo["Rect"].y + 15))
        
        # Botón símbolos (solo visible si está activado)
        simbolos_activados = config["daltonismo"]["simbolos"]

        if simbolos_activados:
            estado_simbolos = "ACTIVADOS"
        else:
            estado_simbolos = "DESACTIVADOS"
        texto_boton_simbolos = fuente.render(f"Símbolos: {estado_simbolos}", True, (255, 255, 255))
        ventana.blit(boton_simbolos["Superficie"], boton_simbolos["Rect"])
        ventana.blit(texto_boton_simbolos, (boton_simbolos["Rect"].x + 30, boton_simbolos["Rect"].y + 15))


def manejar_opciones_volumen(config, ventana, botones, fuente):
    # --- Sección de Volumen ---
        texto_volumen = fuente.render("VOLUMEN", True, (255, 255, 255))
        ventana.blit(texto_volumen, (1280//2 - texto_volumen.get_width()//2, 200))
        
        # Botón bajar volumen (izquierda)
        ventana.blit(botones["bajar_volumen"]["Superficie"], botones["bajar_volumen"]["Rect"])
        
        # Barra de volumen (centrada entre botones)
        volumen_actual = config.get('volumen', 0.7)
        pygame.draw.rect(ventana, (100, 100, 100), (500, 260, 260, 20))  # Fondo gris
        pygame.draw.rect(ventana, (0, 200, 0), (500, 260, int(260 * volumen_actual), 20))  # Barra verde
        
        # Botón subir volumen (derecha)
        ventana.blit(botones["subir_volumen"]["Superficie"], botones["subir_volumen"]["Rect"])
        
        # Porcentaje de volumen (centrado debajo de la barra)
        texto_porcentaje = fuente.render(f"{int(volumen_actual * 100)}%", True, (255, 255, 255))
        ventana.blit(texto_porcentaje, (1280//2 - texto_porcentaje.get_width()//2, 285))

def manejar_botones_opciones(config, ventana, boton_daltonismo,boton_tipo_daltonismo, boton_simbolos, fuente, botones):
    manejar_opciones_daltonismo(config, ventana, boton_daltonismo,boton_tipo_daltonismo, boton_simbolos, fuente)
    manejar_opciones_volumen(config, ventana, botones, fuente)
    ventana.blit(botones["volver"]["Superficie"], botones["volver"]["Rect"])
    pygame.display.flip()

def manejar_mostrar_nombre_usuario(ventana, fondos, boton_input, boton_salir, texto_input, fuente):
    ventana.blit(fondos['menu'], (0, 0))
    
    fuente_titulo = cargar_fuente(36)
    texto_titulo = "Ingrese su nombre"
    render_titulo = fuente_titulo.render(texto_titulo, True, (255, 255, 255))
    rect_titulo = render_titulo.get_rect(center=(640, 170))
    ventana.blit(render_titulo, rect_titulo)
    ventana.blit(boton_input["Superficie"], boton_input["Rect"])
    texto_render = fuente.render(texto_input, True, (255, 255, 255))
    ventana.blit(texto_render, (boton_input["Rect"].x + 30, boton_input["Rect"].y + 15))
    
    ventana.blit(boton_salir["Superficie"], boton_salir["Rect"])
    pygame.display.flip()

def crear_botones_menu_principal(ventana):
    botones_menu = {
        "jugar": crear_boton((300, 70), (490, 320), ventana, (255, 255, 255), "boton-jugar.png"),
        "opciones": crear_boton((300, 70), (490, 400), ventana, (255, 255, 255), "boton-opciones.png"),
        "estadisticas": crear_boton((300, 70), (490, 480), ventana, (255, 255, 255), "boton-estadisticas.png"),
        "salir": crear_boton((300, 70), (490, 560), ventana, (255, 255, 255), "boton-salir.png"),
    }
    return botones_menu

def iniciar_juego(config, ventana, clock, fondos, fuente, max_caracteres, musicas):
    reproducir_musica(musicas['inicio_juego'], config, canal_prioridad=0, loops=0)
    nombre_usuario = mostrar_menu_nombre(ventana, clock, fondos, fuente, max_caracteres, musicas, config)
                    
    if nombre_usuario:
        dificultad = mostrar_menu_dificultad(ventana, clock, fondos, fuente, nombre_usuario, config, musicas)
                        
        if dificultad:
            preguntas = seleccionar_preguntas_por_dificultad(dificultad)
            reproducir_musica(musicas['preguntas_1_5'], config, canal_prioridad=1)
            resultado = jugar_partida(ventana, clock, preguntas, nombre_usuario, dificultad, config, fuente, musicas)
            detener_musica()
            reproducir_musica(musicas['menu'], config, canal_prioridad=0)
