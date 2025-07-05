import os
import re
import json

def escribir_preguntas(lista_preguntas: list, path: str):
    with open(path, "w", encoding = "utf-8") as archivo_preguntas:
        encabezado = "Pregunta;Opciones;Respuesta;Categoria|Dificultad;Descripcion\n"
        archivo_preguntas.write(encabezado)
        for pregunta in lista_preguntas:
            opciones_str = "|".join(pregunta["Opciones"]) #Paso la lista a un solo string
            categoria, dificultad = pregunta["Categoria/Dificultad"] #Se separa categoría y dificultad de la tupla
            linea = (#usar un solo f string, implementar try except
            f"{pregunta["Pregunta"]};"
            f"{opciones_str};"
            f"{pregunta["Respuesta"]};"
            f"{categoria}|{dificultad};"
            f"{pregunta["Descripcion"]}\n"
            )
            archivo_preguntas.write(linea)

def cargar_preguntas(path: str):
    lista_preguntas = []
    with open(path, "r", encoding = "utf-8",) as archivo_preguntas:
        archivo_preguntas.readline()
        for linea in archivo_preguntas:
            registro = re.split(";|\n", linea.strip()) #Le saco los espacios para que no tome \n de ["Descripción"]
            opciones = registro[1].split("|") #Vuelvo a convertirlo en una lista
            categoria, dificultad = registro[3].split("|") #Las separamos para despues convertirlo a tupla
            pregunta = {
                "Pregunta": registro[0],
                "Opciones": opciones,
                "Respuesta": registro[2],
                "Categoria/Dificultad": (categoria, dificultad),
                "Descripcion": registro[4]
            }
            lista_preguntas.append(pregunta)
    return lista_preguntas

def escribir_configuracion(config: dict, path: str):
    with open(path, "w", encoding = "utf-8") as archivo_configuracion:
        json.dump(config, archivo_configuracion, indent = 4, ensure_ascii = False)

def cargar_configuracion(path: str) -> dict:
    with open(path,"r", encoding = "utf-8") as archivo_configuracion:
        archivo_cargado = json.load(archivo_configuracion)
        return archivo_cargado
    
def escribir_estadisticas(lista_estadisticas: list, path: str):
    with open(path, "w", encoding="utf-8") as archivo_estadisticas:
        encabezado = "Usuario;Rondas_jugadas;Preguntas_acertadas;Tiempo_promedio;Contador_partidas_ganadas;Mejor_tiempo\n"
        archivo_estadisticas.write(encabezado)
        for estadistica in lista_estadisticas:
            mejor_tiempo = estadistica["Mejor_tiempo"]
            if mejor_tiempo == float("inf"):
                mejor_tiempo = "--"
            linea = (
                f"{estadistica['Usuario']};"
                f"{estadistica['Rondas_jugadas']};"
                f"{estadistica['Preguntas_acertadas']};"
                f"{estadistica['Tiempo_promedio']};"
                f"{estadistica['Contador_partidas_ganadas']};"
                f"{mejor_tiempo}\n"
            )
            archivo_estadisticas.write(linea)


def leer_estadisticas(path: str) -> list:
    """Lee estadísticas desde un CSV y devuelve una lista de diccionarios."""
    estadisticas = []

    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as archivo:
            archivo.readline()  # Saltear encabezado
            for linea in archivo:
                linea = linea.strip()
                if linea != "":
                    llave = linea.split(";")
                    if llave[5] == "--":
                        mejor_tiempo = float("inf")
                    else:
                        mejor_tiempo = float(llave[5])
                    estadistica = {
                        "Usuario": llave[0],
                        "Rondas_jugadas": int(llave[1]),
                        "Preguntas_acertadas": int(llave[2]),
                        "Tiempo_promedio": float(llave[3]),
                        "Contador_partidas_ganadas": int(llave[4]),
                        "Mejor_tiempo": mejor_tiempo
                    }
                    estadisticas.append(estadistica)

    return estadisticas