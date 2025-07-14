# utils.py - Funciones reutilizables del proyecto

import pygame
import json
import emoji
import sys
from configuraciones import guardar_configuracion

# --------------------------
# Utilidades de archivos
# --------------------------
def cargar_preguntas(path):
    """Carga preguntas desde CSV"""
    with open(path, encoding='utf-8') as archivo:
        lineas = archivo.readlines()[1:]
        preguntas = []
        for linea in lineas:
            partes = linea.strip().split(";")
            if len(partes) == 5:
                pregunta, opciones, respuesta, cat_dif, descripcion = partes
                opciones = opciones.split("|")
                categoria, dificultad = cat_dif.split("|")
                preguntas.append({
                    "pregunta": pregunta,
                    "opciones": opciones,
                    "respuesta": respuesta,
                    "categoria": categoria,
                    "dificultad": dificultad.lower(),
                    "descripcion": descripcion
                })
        return preguntas

def leer_estadisticas(path):
    """Lee estadísticas desde CSV"""
    datos = []
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            archivo.readline()  # Saltar encabezado
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    partes = linea.split(";")
                    if partes[5] == "--":
                        mejor_tiempo = float("inf")
                    else:
                        mejor_tiempo = float(partes[5])
                    estadistica = {
                        "Usuario": partes[0],
                        "Partidas_jugadas": int(partes[1]),
                        "Preguntas_acertadas": int(partes[2]),
                        "Tiempo_promedio": float(partes[3]),
                        "Contador_partidas_ganadas": int(partes[4]),
                        "Mejor_tiempo": mejor_tiempo
                    }
                    datos.append(estadistica)
    except Exception:
        datos = []
    return datos

def escribir_estadisticas(lista_estadisticas, path):
    """Escribe estadísticas a CSV (funciones_genericas_archivos)"""
    encabezado = "Usuario;Partidas_jugadas;Preguntas_acertadas;Tiempo_promedio;Contador_partidas_ganadas;Mejor_tiempo\n"
    try:
        with open(path, "w", encoding="utf-8") as archivo:
            archivo.write(encabezado)
            for est in lista_estadisticas:
                mejor_tiempo = est["Mejor_tiempo"]
                if mejor_tiempo == float("inf"):
                    mejor_tiempo = "--"
                linea = f"{est['Usuario']};{est['Partidas_jugadas']};{est['Preguntas_acertadas']};{est['Tiempo_promedio']};{est['Contador_partidas_ganadas']};{mejor_tiempo}\n"
                archivo.write(linea)
    except Exception as error:
        print(f"Error al escribir estadísticas en {path}: {error}")

# --------------------------
# Utilidades de UI
# --------------------------
def crear_boton(dimension, posicion, ventana, color_borde, path_imagen=None):
    """Crea un botón (Boton.py)"""
    boton = {}
    boton["Ventana"] = ventana
    boton["Dimension"] = dimension
    boton["Posicion"] = posicion
    boton["ColorBorde"] = color_borde

    if path_imagen:
        img = pygame.image.load(path_imagen)
        boton["Superficie"] = pygame.transform.scale(img, dimension)
    else:
        boton["Superficie"] = pygame.Surface(dimension)
        boton["Superficie"].fill("gray")

    boton["Rect"] = pygame.Rect(posicion, dimension)
    return boton

def dibujar_texto(ventana, texto, x, y, color=(255, 255, 255)):
    """Dibuja texto en pantalla (main_pygame)"""
    fuente = pygame.font.SysFont("Segoe UI Emoji", 28)
    render = fuente.render(emoji.emojize(texto, language="alias"), True, color)
    ventana.blit(render, (x, y))

# --------------------------
# Utilidades de estadísticas
# --------------------------
def guardar_estadistica(nombre, modo, partidas, acertadas, tiempos_preguntas, ganadas, mejor_tiempo):
    """Guarda estadísticas de una partida (funciones_juego)"""
    path = f"estadisticas_{modo}.csv"
    lista = leer_estadisticas(path)

    tiempo_prom = round(sum(tiempos_preguntas) / len(tiempos_preguntas), 2) if tiempos_preguntas else 0

    # Buscar usuario existente
    for est in lista:
        if est["Usuario"] == nombre:
            # Actualizar estadísticas
            est["Partidas_jugadas"] += partidas
            est["Preguntas_acertadas"] += acertadas
            est["Contador_partidas_ganadas"] += ganadas
            
            # Calcular nuevo tiempo promedio ponderado
            if est["Partidas_jugadas"] > 0:
                est["Tiempo_promedio"] = round((est["Tiempo_promedio"] * (est["Partidas_jugadas"] - partidas) + sum(tiempos_preguntas)) / est["Partidas_jugadas"], 2)
            
            # Actualizar mejor tiempo
            if mejor_tiempo < est["Mejor_tiempo"]:
                est["Mejor_tiempo"] = mejor_tiempo
                
            break
    else:
        # Crear nueva entrada si no existe
        lista.append({
            "Usuario": nombre,
            "Partidas_jugadas": partidas,
            "Preguntas_acertadas": acertadas,
            "Tiempo_promedio": tiempo_prom,
            "Contador_partidas_ganadas": ganadas,
            "Mejor_tiempo": mejor_tiempo
        })
    
    escribir_estadisticas(lista, path)

# --------------------------
# Utilidades de configuración
# --------------------------
def cargar_configuracion(path):
    """Carga configuración desde JSON (funciones_genericas_archivos)"""
    archivo = {}
    try:
        with open(path,"r", encoding="utf-8") as archivo_configuracion:
            archivo = json.load(archivo_configuracion)
    except Exception as error:
        print(f"Error al cargar configuración desde {path}: {error}")
    return archivo

# --------------------------
# Utilidades de texto
# --------------------------
def dividir_texto_multilinea(texto, fuente, max_ancho):
    """Divide texto en múltiples líneas (funciones_juego)"""
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        test_linea = linea_actual + palabra + " "
        if fuente.size(test_linea)[0] <= max_ancho:
            linea_actual = test_linea
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "
    if linea_actual:
        lineas.append(linea_actual.strip())

    return lineas

# --------------------------
# Formateadores de datos
# --------------------------
def formatear_pregunta_csv(pregunta):
    """Formatea pregunta para CSV (funciones_puras_archivos)"""
    opciones_str = "|".join(pregunta["Opciones"])
    categoria, dificultad = pregunta["Categoria/Dificultad"]
    linea = f"{pregunta['Pregunta']};{opciones_str};{pregunta['Respuesta']};{categoria}|{dificultad};{pregunta['Descripcion']}\n"
    return linea

def formatear_estadistica_csv(estadistica):
    """Formatea estadística para CSV (funciones_puras_archivos)"""
    mejor_tiempo = estadistica["Mejor_tiempo"]
    if mejor_tiempo == float("inf"):
        mejor_tiempo = "--"
    linea = f"{estadistica['Usuario']};{estadistica['Partidas_jugadas']};{estadistica['Preguntas_acertadas']};{estadistica['Tiempo_promedio']};{estadistica['Contador_partidas_ganadas']};{mejor_tiempo}\n"
    return linea

def salir_del_juego(config):
    guardar_configuracion("config.json", config)
    pygame.quit()
    sys.exit()