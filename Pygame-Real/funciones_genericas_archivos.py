import json
from funciones_puras_archivos import *

def escribir_configuracion(config: dict, path: str):
    try:
        with open(path, "w", encoding="utf-8") as archivo_configuracion:
            json.dump(config, archivo_configuracion, indent=4, ensure_ascii=False)
    except Exception as error:
        print(f"Error al guardar configuración en {path}: {error}")

def cargar_configuracion(path: str) -> dict:
    archivo = {}
    try:
        with open(path,"r", encoding="utf-8") as archivo_configuracion:
            archivo = json.load(archivo_configuracion)
    except Exception as error:
        print(f"Error al cargar configuración desde {path}: {error}")
    return archivo
        
def escribir_datos_formateados_a_csv(path: str, lista_datos: list, funcion_formatear, encabezado: str):
    try:
        with open(path, "w", encoding="utf-8") as archivo:
            archivo.write(encabezado)
            for dato in lista_datos:
                linea = funcion_formatear(dato)
                archivo.write(linea)
    except Exception as error:
        print(f"Error al escribir datos en {path}: {error}")

def leer_datos_csv(path: str, funcion_leer_linea) -> list:
    datos = []
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            archivo.readline()  # Saltar encabezado
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    dato = funcion_leer_linea(linea)
                    if dato is not None:
                        datos.append(dato)
                    else:
                        print(f"⚠️ Error de formato detectado: {linea}")
    except Exception:
        datos = []
    return datos

def escribir_preguntas(lista_preguntas: list, path: str):
    encabezado = "Pregunta;Opciones;Respuesta;Categoria|Dificultad;Descripcion\n"
    return escribir_datos_formateados_a_csv(path, lista_preguntas, formatear_pregunta_csv, encabezado)

def cargar_preguntas(path: str) -> list:
    return leer_datos_csv(path, leer_linea_pregunta)

def escribir_estadisticas(lista_estadisticas: list, path: str):
    encabezado = "Usuario;Partidas_jugadas;Preguntas_acertadas;Tiempo_promedio;Contador_partidas_ganadas;Mejor_tiempo\n"
    return escribir_datos_formateados_a_csv(path, lista_estadisticas, formatear_estadistica_csv, encabezado)

def leer_estadisticas(path: str) -> list:
    return leer_datos_csv(path, leer_linea_estadisticas)