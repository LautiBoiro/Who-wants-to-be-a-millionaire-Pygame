import pygame
import sys
from funciones_genericas_archivos import leer_estadisticas, escribir_estadisticas
from daltonismo import agregar_simbolos

# ======================== CONSTANTES ========================
PREMIOS = [100000, 200000, 300000, 400000, 600000, 800000, 1200000]
NIVELES_SALVAVIDAS = [3, 5]
COLORES_DALTONISMO = {
    "protanopia": {
        "correcto": (0, 150, 255),
        "incorrecto": (255, 255, 0)
    },
    "deuteranopia": {
        "correcto": (0, 100, 255),
        "incorrecto": (255, 165, 0)
    },
    "tritanopia": {
        "correcto": (0, 200, 0),
        "incorrecto": (255, 105, 180)
    }
}
COLORES_NORMALES = {
    "correcto": (0, 255, 0),
    "incorrecto": (255, 0, 0)
}
COLOR_SOMBRA = (0, 0, 0)

# ======================== FUNCIONES PURAS ========================

def obtener_config_daltonismo(config):
    """
    Extrae la configuración de daltonismo del objeto config.
    Función pura que solo lee datos.
    """
    if not config:
        return False, None, False
    
    daltonismo_config = config.get("daltonismo", {})
    activado = daltonismo_config.get("activado", False)
    tipo = daltonismo_config.get("tipo", "protanopia") if activado else None
    usar_simbolos = daltonismo_config.get("simbolos", True) if activado else False
    
    return activado, tipo, usar_simbolos

def obtener_imagenes_daltonismo(daltonismo_activado, tipo_daltonismo):
    """
    Retorna las rutas de las imágenes según la configuración de daltonismo.
    Función pura.
    """
    if daltonismo_activado and tipo_daltonismo:
        return (f"boton-{tipo_daltonismo}-correcto.png", 
                f"boton-{tipo_daltonismo}-incorrecto.png")
    return ("boton-normal-verde.png", "boton-normal-rojo.png")

def obtener_colores_daltonismo(daltonismo_activado, tipo_daltonismo):
    """
    Retorna los colores para indicadores según la configuración de daltonismo.
    Función pura.
    """
    if daltonismo_activado and tipo_daltonismo in COLORES_DALTONISMO:
        return COLORES_DALTONISMO[tipo_daltonismo]
    return COLORES_NORMALES

def calcular_posicion_nivel(indice, total_niveles):
    """
    Calcula la posición Y para un nivel en el pozo de premios.
    Función pura.
    """
    return 50 + (total_niveles - 1 - indice) * 55

def obtener_color_nivel(nivel_mostrado, nivel_actual, niveles_salvavidas):
    """
    Determina los colores para mostrar un nivel específico.
    Función pura.
    """
    color_num = (255, 215, 0) if nivel_mostrado == nivel_actual else (255, 255, 255)
    color_monto = (255, 215, 0) if nivel_mostrado in niveles_salvavidas else (255, 255, 255)
    return color_num, color_monto

def formatear_monto(monto):
    """
    Formatea un monto para mostrar con separadores de miles.
    Función pura.
    """
    return f"${monto:,}".replace(",", ".")

def dividir_texto_multilinea(texto, fuente, max_ancho):
    """
    Divide un texto en múltiples líneas según el ancho máximo.
    Función pura.
    """
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        test_linea = linea_actual + palabra + " "
        if fuente.size(test_linea)[0] <= max_ancho:
            linea_actual = test_linea
        else:
            if linea_actual.strip():
                lineas.append(linea_actual.strip())
            linea_actual = palabra + " "
    
    if linea_actual.strip():
        lineas.append(linea_actual.strip())

    return lineas

def filtrar_preguntas_por_dificultad(preguntas: list, dificultad_objetivo: str) -> list:
    """
    Filtra una lista de preguntas, devolviendo solo aquellas cuya dificultad coincida
    con la dificultad objetivo (sin importar mayúsculas/minúsculas).
    
    Parámetros:
        preguntas (list): Lista de diccionarios con preguntas.
        dificultad_objetivo (str): Dificultad que queremos filtrar ("facil", "medio", "dificil", etc).
    
    Retorna:
        list: Lista filtrada de preguntas que cumplen con la dificultad dada.
    """
    preguntas_filtradas = []
    
    for pregunta in preguntas:
        dificultad = pregunta.get("dificultad", "").lower()
        if dificultad == dificultad_objetivo.lower():
            preguntas_filtradas.append(pregunta)
    
    return preguntas_filtradas

def seleccionar_preguntas_segun_modo(faciles, medias, dificiles, modo):
    """
    Selecciona preguntas según el modo de dificultad.
    Función pura.
    """
    selecciones = {
        "facil": faciles[:4] + medias[:3],
        "normal": faciles[:3] + medias[:2] + dificiles[:2],
        "dificil": medias[:4] + dificiles[:3],
        "extremo": dificiles[:7]
    }
    return selecciones.get(modo, [])

def calcular_tiempo_promedio(tiempos_anteriores, nuevos_tiempos, partidas_anteriores, nuevas_partidas):
    """
    Calcula el tiempo promedio actualizado.
    Función pura.
    """
    if not nuevos_tiempos:
        return tiempos_anteriores
    
    total_partidas = partidas_anteriores + nuevas_partidas
    if total_partidas == 0:
        return 0
    
    tiempo_acumulado_anterior = tiempos_anteriores * partidas_anteriores
    tiempo_acumulado_nuevo = sum(nuevos_tiempos)
    
    return round((tiempo_acumulado_anterior + tiempo_acumulado_nuevo) / total_partidas, 2)

def crear_estadistica_nueva(nombre, partidas, acertadas, tiempos_preguntas, ganadas, mejor_tiempo):
    """
    Crea una nueva entrada de estadísticas.
    Función pura.
    """
    tiempo_prom = round(sum(tiempos_preguntas) / len(tiempos_preguntas), 2) if tiempos_preguntas else 0
    
    return {
        "Usuario": nombre,
        "Partidas_jugadas": partidas,
        "Preguntas_acertadas": acertadas,
        "Tiempo_promedio": tiempo_prom,
        "Contador_partidas_ganadas": ganadas,
        "Mejor_tiempo": mejor_tiempo
    }

def actualizar_estadistica_existente(estadistica, partidas, acertadas, tiempos_preguntas, ganadas, mejor_tiempo):
    """
    Actualiza una estadística existente.
    Función pura que retorna una nueva estadística.
    """
    nueva_estadistica = estadistica.copy()
    
    nueva_estadistica["Partidas_jugadas"] += partidas
    nueva_estadistica["Preguntas_acertadas"] += acertadas
    nueva_estadistica["Contador_partidas_ganadas"] += ganadas
    
    if nueva_estadistica["Partidas_jugadas"] > 0:
        nueva_estadistica["Tiempo_promedio"] = calcular_tiempo_promedio(
            estadistica["Tiempo_promedio"],
            tiempos_preguntas,
            estadistica["Partidas_jugadas"] - partidas,
            partidas
        )
    
    if mejor_tiempo < nueva_estadistica["Mejor_tiempo"]:
        nueva_estadistica["Mejor_tiempo"] = mejor_tiempo
    
    return nueva_estadistica

# ======================== FUNCIONES DE RENDERIZADO ========================

def dibujar_fondo_y_pozo(ventana, fondo, fondo_pozo):
    """
    Dibuja el fondo principal y el fondo del pozo.
    """
    ventana.blit(fondo, (0, 0))
    ventana.blit(fondo_pozo, (1000, 20))

def dibujar_nivel_premio(ventana, fuente, nivel, premio, posicion_y, nivel_actual, niveles_salvavidas):
    """
    Dibuja un nivel específico del pozo de premios.
    """
    color_num, color_monto = obtener_color_nivel(nivel, nivel_actual, niveles_salvavidas)
    
    texto_num = fuente.render(f"{nivel}.", True, color_num)
    texto_monto = fuente.render(formatear_monto(premio), True, color_monto)
    
    ventana.blit(texto_num, (1040, posicion_y))
    ventana.blit(texto_monto, (1040 + texto_num.get_width() + 10, posicion_y))

def dibujar_niveles_premios(ventana, fuente, nivel_actual):
    """
    Dibuja todos los niveles del pozo de premios.
    """
    for i, premio in enumerate(PREMIOS):
        nivel_mostrado = i + 1
        posicion_y = calcular_posicion_nivel(i, len(PREMIOS))
        dibujar_nivel_premio(ventana, fuente, nivel_mostrado, premio, posicion_y, nivel_actual, NIVELES_SALVAVIDAS)

def dibujar_pregunta(ventana, fuente, pregunta_texto):
    """
    Dibuja el texto de la pregunta.
    """
    texto_pregunta = fuente.render(pregunta_texto, True, (255, 255, 255))
    ventana.blit(texto_pregunta, (50, 50))

def cargar_imagen_boton(ruta_imagen, dimension):
    """
    Carga y escala una imagen para un botón.
    """
    try:
        img = pygame.image.load(ruta_imagen).convert_alpha()
        return pygame.transform.scale(img, dimension)
    except:
        # Imagen de respaldo
        img_respaldo = "boton-normal.png" if "normal" in ruta_imagen else "boton-normal-verde.png"
        img = pygame.image.load(img_respaldo).convert_alpha()
        return pygame.transform.scale(img, dimension)

def actualizar_estado_boton(boton, es_correcta, es_incorrecta, img_correcta, img_incorrecta):
    """
    Actualiza el estado visual de un botón según la respuesta.
    """
    if es_correcta:
        img = cargar_imagen_boton(img_correcta, boton["Dimension"])
    elif es_incorrecta:
        img = cargar_imagen_boton(img_incorrecta, boton["Dimension"])
    else:
        img = cargar_imagen_boton("boton-normal.png", boton["Dimension"])
    
    boton["Imagenes"]["normal"] = img
    boton["Imagenes"]["hover"] = img
    boton["Estado"] = "normal"

def dibujar_indicador_respuesta(ventana, fuente_indicadores, rect_boton, es_correcta, es_incorrecta, colores):
    """
    Dibuja el indicador de respuesta correcta o incorrecta.
    """
    if es_correcta:
        texto = "✓ Respuesta correcta"
        color = colores["correcto"]
    elif es_incorrecta:
        texto = "✗ Respuesta incorrecta"
        color = colores["incorrecto"]
    else:
        return
    
    # Sombra
    texto_sombra = fuente_indicadores.render(texto, True, COLOR_SOMBRA)
    ventana.blit(texto_sombra, (rect_boton.x + 52, rect_boton.y + 72))
    
    # Texto principal
    texto_principal = fuente_indicadores.render(texto, True, color)
    ventana.blit(texto_principal, (rect_boton.x + 50, rect_boton.y + 70))

def dibujar_boton_respuesta(ventana, fuente, boton, opcion, indice, respuesta_correcta, respuesta_incorrecta, img_correcta, img_incorrecta, colores):
    """
    Dibuja un botón de respuesta completo.
    """
    if not opcion:
        return
    
    es_correcta = respuesta_correcta is not None and indice == respuesta_correcta
    es_incorrecta = respuesta_incorrecta is not None and indice == respuesta_incorrecta
    
    # SOLO actualizar imágenes si hay una respuesta seleccionada
    if respuesta_correcta is not None or respuesta_incorrecta is not None:
        if es_correcta:
            img = cargar_imagen_boton(img_correcta, boton["Dimension"])
            # Solo cambiar la imagen normal, NO la hover
            boton["Imagenes"]["normal"] = img
        elif es_incorrecta:
            img = cargar_imagen_boton(img_incorrecta, boton["Dimension"])
            # Solo cambiar la imagen normal, NO la hover
            boton["Imagenes"]["normal"] = img
        else:
            # Restaurar imagen original si no es correcta ni incorrecta
            if "ImagenesOriginales" in boton:
                boton["Imagenes"]["normal"] = boton["ImagenesOriginales"]["normal"].copy()
    
    # Dibujar botón según su estado actual
    ventana.blit(boton["Imagenes"][boton["Estado"]], boton["Rect"])
    
    # Dibujar texto de la opción
    texto_opcion = fuente.render(opcion, True, (255, 255, 255))
    ventana.blit(texto_opcion, (boton["Rect"].x + 50, boton["Rect"].y + 15))
    
    # Dibujar indicador
    fuente_indicadores = pygame.font.SysFont("Segoe UI Emoji", 20)
    dibujar_indicador_respuesta(ventana, fuente_indicadores, boton["Rect"], es_correcta, es_incorrecta, colores)

def dibujar_descripcion(ventana, fuente, fondo_descripcion, descripcion):
    """
    Dibuja la descripción de la pregunta.
    """
    ventana.blit(fondo_descripcion, (50, 530))
    lineas_desc = dividir_texto_multilinea(descripcion, fuente, 770)
    for idx, linea in enumerate(lineas_desc):
        render_linea = fuente.render(linea, True, (200, 200, 200))
        ventana.blit(render_linea, (90, 550 + idx * 30))

def dibujar_tiempo_restante(ventana, fuente, tiempo_restante):
    """
    Dibuja el tiempo restante.
    """
    if tiempo_restante is not None:
        texto_tiempo = fuente.render(f"{int(tiempo_restante)}", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (1100, 650))

# ======================== FUNCIONES PRINCIPALES ========================

def dibujar_pregunta_y_opciones(ventana, pregunta, fuente, fondo, botones_respuesta, nivel_actual, fondo_pozo, fondo_descripcion, respuesta_correcta=None, respuesta_incorrecta=None, mostrar_descripcion=False, tiempo_restante=None, config=None):
    """
    Función principal para dibujar la pregunta y opciones.
    Orquesta las funciones más pequeñas.
    """
    # Obtener configuración
    daltonismo_activado, tipo_daltonismo, usar_simbolos = obtener_config_daltonismo(config)
    img_correcta, img_incorrecta = obtener_imagenes_daltonismo(daltonismo_activado, tipo_daltonismo)
    colores = obtener_colores_daltonismo(daltonismo_activado, tipo_daltonismo)
    
    # Dibujar elementos base
    dibujar_fondo_y_pozo(ventana, fondo, fondo_pozo)
    dibujar_niveles_premios(ventana, fuente, nivel_actual)
    dibujar_pregunta(ventana, fuente, pregunta["pregunta"])
    
    # Preparar opciones
    opciones_mostradas = pregunta["opciones"]
    if daltonismo_activado and usar_simbolos:
        opciones_mostradas = agregar_simbolos(pregunta["opciones"])
    
    # Dibujar botones de respuesta
    for i, opcion in enumerate(opciones_mostradas):
        dibujar_boton_respuesta(
            ventana, fuente, botones_respuesta[i], opcion, i,
            respuesta_correcta, respuesta_incorrecta,
            img_correcta, img_incorrecta, colores
        )
    
    # Dibujar descripción si es necesario
    if mostrar_descripcion:
        dibujar_descripcion(ventana, fuente, fondo_descripcion, pregunta["descripcion"])
    
    # Dibujar tiempo restante
    dibujar_tiempo_restante(ventana, fuente, tiempo_restante)
    
    pygame.display.flip()

def seleccionar_preguntas_por_dificultad(dificultad):
    """
    Selecciona preguntas según la dificultad especificada.
    """
    from funciones_archivos import cargar_preguntas
    
    preguntas = cargar_preguntas("preguntas.csv")
    
    # Filtrar por dificultad
    faciles = filtrar_preguntas_por_dificultad(preguntas, "facil")
    medias = filtrar_preguntas_por_dificultad(preguntas, "medio")
    dificiles = filtrar_preguntas_por_dificultad(preguntas, "dificil")
    
    return seleccionar_preguntas_segun_modo(faciles, medias, dificiles, dificultad)

def guardar_estadistica(nombre, modo, partidas, acertadas, tiempos_preguntas, ganadas, mejor_tiempo):
    """
    Guarda las estadísticas de un jugador.
    """
    path = f"estadisticas_{modo}.csv"
    lista = leer_estadisticas(path)
    
    # Buscar estadística existente
    estadistica_encontrada = None
    indice_encontrado = None
    
    for i, est in enumerate(lista):
        if est["Usuario"] == nombre:
            estadistica_encontrada = est
            indice_encontrado = i
            break
    
    if estadistica_encontrada:
        # Actualizar estadística existente
        nueva_estadistica = actualizar_estadistica_existente(
            estadistica_encontrada, partidas, acertadas, tiempos_preguntas, ganadas, mejor_tiempo
        )
        lista[indice_encontrado] = nueva_estadistica
    else:
        # Crear nueva estadística
        nueva_estadistica = crear_estadistica_nueva(
            nombre, partidas, acertadas, tiempos_preguntas, ganadas, mejor_tiempo
        )
        lista.append(nueva_estadistica)
    
    escribir_estadisticas(lista, path)