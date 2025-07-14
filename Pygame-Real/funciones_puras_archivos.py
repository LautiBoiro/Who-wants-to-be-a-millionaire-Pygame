import re

def formatear_pregunta_csv(pregunta: dict) -> str:
    opciones_str = "|".join(pregunta["Opciones"])  # Convierte lista a string
    categoria, dificultad = pregunta["Categoria/Dificultad"]
    linea = f"{pregunta['Pregunta']};{opciones_str};{pregunta['Respuesta']};{categoria}|{dificultad};{pregunta['Descripcion']}\n"
    return linea

def formatear_estadistica_csv(estadistica: dict) -> str:
    mejor_tiempo = estadistica["Mejor_tiempo"]
    if mejor_tiempo == float("inf"):
        mejor_tiempo = "--"
    linea = f"{estadistica['Usuario']};{estadistica['Partidas_jugadas']};{estadistica['Preguntas_acertadas']};{estadistica['Tiempo_promedio']};{estadistica['Contador_partidas_ganadas']};{mejor_tiempo}\n"
    return linea

def leer_linea_pregunta(linea: str) -> dict | None:
    try:
        registro = re.split(";|\n", linea.strip())
        opciones = registro[1].split("|")
        categoria, dificultad = registro[3].split("|")
        pregunta = {
            "Pregunta": registro[0],
            "Opciones": opciones,
            "Respuesta": registro[2],
            "Categoria/Dificultad": (categoria, dificultad),
            "Descripcion": registro[4]
        }
    except (IndexError, ValueError):
        return None
    return pregunta

def leer_linea_estadisticas(linea: str) -> dict | None:
    try:
        llave = linea.split(";")
        if llave[5] == "--":
            mejor_tiempo = float("inf")
        else:
            mejor_tiempo = float(llave[5])
        estadistica = {
            "Usuario": llave[0],
            "Partidas_jugadas": int(llave[1]),
            "Preguntas_acertadas": int(llave[2]),
            "Tiempo_promedio": float(llave[3]),
            "Contador_partidas_ganadas": int(llave[4]),
            "Mejor_tiempo": mejor_tiempo
        }
    except (IndexError, ValueError):
        return None
    return estadistica